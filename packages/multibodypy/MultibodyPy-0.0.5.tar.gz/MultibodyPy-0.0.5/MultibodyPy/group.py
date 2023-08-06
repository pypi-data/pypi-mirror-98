import numpy as np
from . import bodies, forces, constraints, solver
from .scipy_integrate_modified.radau import Radau
from .scipy_integrate_modified.bdf import BDF
from scipy import sparse, integrate
from functools import partialmethod
from scipy import optimize
import csv
import dill as pickle
import multiprocessing
import concurrent.futures
from numba import int32, float32
from numba.experimental import jitclass


class Group:
    def __init__(self, body, force, constraint, moving_marker=[], animated_ground=[], stabilization='GGL',
                 data_filename='data.csv', save_acceleration=False, save_constraint_forces=False, animation_filename='animation.bin'):
        self.bodies = [b for b in body if type(b) is not bodies.Ground]
        self.n = len(self.bodies)
        self.forces = force
        self.constraints = constraint
        self.moving_marker = moving_marker
        self.animated_ground = animated_ground

        self.numDof = self.set_num_dof
        self.dim_y = self.dimension_y()
        self.dim_z = self.dimension_z()

        self.qglobal = self.initialize_qglobal
        self.q0global = self.qglobal
        self.y_global = self.qglobal[0:self.dim_y]
        self.z_global = self.qglobal[self.dim_y:self.dim_y + self.dim_z]

        self.solve = self.assemble_mass
        self.qe = self.assemble_force()

        self.qd = np.zeros(self.numDof)
        self.g1 = []
        self.stabilization = stabilization

        self.save_acceleration = save_acceleration
        self.save_constraint_forces = save_constraint_forces
        header = self.get_header()
        self.data_saver = DataSaver(data_filename, header)

        self.animation_saver = AnimationSaver(animation_filename)

        self.Jg = 0
        self.la = 0

        self.initialize_g()
        self.t_eval = []
        self.dt_eval = 0

    def qdot(self, t, qglobal, update=False):
        self.update_system(t, qglobal)

        # get global global jacobian and Lagrange-Multiplicators
        c_global = 0
        if len(self.constraints) > 0:
            Jg, Jgpz = self.jacobi_constraint()

            # Stabilization
            # Gear-Gupta-Leimkuhler
            if self.stabilization == 'GGL':
                la, mue = self.lagrange_multiplicators(self.z_global, Jg, Jgpz)
                c_global = np.dot(Jg.transpose(), la)
                self.c_global = c_global
                import ipdb
                ipdb.set_trace()
                self.z_global = self.z_global + np.dot(Jg.transpose(), mue)
                self.update_body_velocities(
                    np.concatenate((self.y_global, self.z_global)))
            elif self.stabilization == 'Baumgarte':
                g = self.g_global()
                gp = np.dot(Jg, self.z_global)
                la = self.lagrange_baumgarte(g, gp, Jg, Jgpz)
                c_global = np.dot(Jg.transpose(), la)
            else:
                la, mue = self.lagrange_multiplicators(self.z_global, Jg, Jgpz)
                c_global = np.dot(Jg.transpose(), la)
                self.c_global = c_global

            # Update constraint Forces
            for c in self.constraints:
                if c.save is True:
                    c.update_constraint_force(c_global)

            # Add constraint dampings
            for con in self.constraints:
                if isinstance(con, (constraints.Joint, constraints.Hinge)):
                    self.add_constraint_damping(con)
            self.qe = self.forces_global

            # Update all constraint forces
            self.qe = self.qe + c_global

            # Update Jacobian and Lambda
            self.Jg = Jg
            self.la = la

        # get kinematic ode
        yp_global = self.kinematic_ode_global

        # dynamic ode
        zp_global = sparse.linalg.spsolve(self.solve, self.qe)

        # state change
        qp_global = np.concatenate((yp_global, zp_global))

        if self.save_acceleration:
            for body in self.bodies:
                body.update_acceleration(qp_global)

        return qp_global

    def update_system(self, t, qglobal):
        # Update locations of moving marker if not empty
        if self.moving_marker:
            self.update_moving_marker(t)

        # Update state of bodies
        self.update_body_states(t, qglobal)

        # get global y and z
        y_global, z_global = self.get_position_velocity
        self.y_global = y_global
        self.z_global = z_global

        # Apply forces to bodies
        self.update_body_forces()

        # get global forces
        self.qe = self.forces_global

    def update_body_forces(self):
        for f in self.forces:
            F1, M1, F2, M2 = f.get_force()
            f.body1.add_external_force_moment(F1, M1)
            f.body2.add_external_force_moment(F2, M2)

    def update_moving_marker(self, t):
        for mm in self.moving_marker:
            mm.update_location(t)

    def dimension_y(self):
        dim = 0
        for body in self.bodies:
            if type(body) is bodies.RigidBody1D:
                dim += 1
            else:
                dim += 7
        return dim

    def dimension_z(self):
        dim = 0
        for body in self.bodies:
            if type(body) is bodies.RigidBody1D:
                dim += 1
            else:
                dim += 6
        return dim
    #
    # def save_forces_positions(self):
    #     for f in self.forces:
    #         if f.save is True:
    #             f.force_saver.save(f.F1)
    #     for mm in self.moving_marker:
    #         if mm.save is True or mm.animation is not None:
    #             mm.position_saver.save(mm.rSPK)

    def save_data(self, t, dt):
        data = {}
        data['Time'] = t
        data['Step'] = dt
        for mm in self.moving_marker:
            if mm.save == True:
                data[mm.name + '_x'] = mm.r0P0[0]
                data[mm.name + '_y'] = mm.r0P0[1]
                data[mm.name + '_z'] = mm.r0P0[2]
        for f in self.forces:
            if f.save is True:
                data[f.name + '_x'] = f.F1[0]
                data[f.name + '_y'] = f.F1[1]
                data[f.name + '_z'] = f.F1[2]
                data[f.name + '_mx'] = f.M1[0]
                data[f.name + '_my'] = f.M1[1]
                data[f.name + '_mz'] = f.M1[2]
        for c in self.constraints:
            if c.save is True:
                data_c = c.get_constraint_force()
                data.update(data_c)
        for b in self.bodies:
            if type(b) is bodies.RigidBody:
                data[b.name + '_x'] = b.r0S0[0]
                data[b.name + '_y'] = b.r0S0[1]
                data[b.name + '_z'] = b.r0S0[2]
                data[b.name + '_pE0'] = b.pE[0]
                data[b.name + '_pE1'] = b.pE[1]
                data[b.name + '_pE2'] = b.pE[2]
                data[b.name + '_pE3'] = b.pE[2]
                data[b.name + '_vx'] = b.v0S0[0]
                data[b.name + '_vy'] = b.v0S0[1]
                data[b.name + '_vz'] = b.v0S0[2]
                data[b.name + '_omx'] = b.om0KK[0]
                data[b.name + '_omy'] = b.om0KK[1]
                data[b.name + '_omz'] = b.om0KK[2]
                if self.save_acceleration:
                    data[b.name + '_ax'] = b.a0S0[0]
                    data[b.name + '_ay'] = b.a0S0[1]
                    data[b.name + '_az'] = b.a0S0[2]
                    data[b.name + '_omxp'] = b.om0KKp[0]
                    data[b.name + '_omyp'] = b.om0KKp[1]
                    data[b.name + '_omzp'] = b.om0KKp[2]
            elif type(b) is bodies.RigidBody1D:
                data[b.name + '_r'] = b.r
                data[b.name + '_v'] = b.v

        self.data_saver.save(data)

    def get_save_data(self, t, dt):
        data = {}
        data['Time'] = t
        data['Step'] = dt
        for f in self.forces:
            if f.save is True:
                data[f.name + '_x'] = f.F1[0]
                data[f.name + '_y'] = f.F1[1]
                data[f.name + '_z'] = f.F1[2]
                data[f.name + '_mx'] = f.M1[0]
                data[f.name + '_my'] = f.M1[1]
                data[f.name + '_mz'] = f.M1[2]
        for c in self.constraints:
            if c.save is True:
                data_c = c.get_constraint_force()
                data.update(data_c)
        for b in self.bodies:
            if type(b) is bodies.RigidBody:
                data[b.name + '_x'] = b.r0S0[0]
                data[b.name + '_y'] = b.r0S0[1]
                data[b.name + '_z'] = b.r0S0[2]
                data[b.name + '_pE0'] = b.pE[0]
                data[b.name + '_pE1'] = b.pE[1]
                data[b.name + '_pE2'] = b.pE[2]
                data[b.name + '_pE3'] = b.pE[2]
                data[b.name + '_vx'] = b.v0S0[0]
                data[b.name + '_vy'] = b.v0S0[1]
                data[b.name + '_vz'] = b.v0S0[2]
                data[b.name + '_omx'] = b.om0KK[0]
                data[b.name + '_omy'] = b.om0KK[1]
                data[b.name + '_omz'] = b.om0KK[2]
                if self.save_acceleration:
                    data[b.name + '_ax'] = b.a0S0[0]
                    data[b.name + '_ay'] = b.a0S0[1]
                    data[b.name + '_az'] = b.a0S0[2]
                    data[b.name + '_omxp'] = b.om0KKp[0]
                    data[b.name + '_omyp'] = b.om0KKp[1]
                    data[b.name + '_omzp'] = b.om0KKp[2]
            elif type(b) is bodies.RigidBody1D:
                data[b.name + '_r'] = b.r
                data[b.name + '_v'] = b.v
        return data

    def save_animation(self, t, q):
        self.animation_saver.save(
            t, q, [*self.bodies, *self.animated_ground], self.moving_marker, self.dim_y)

    def save_constraints(self):
        for c in self.constraints:
            if c.save is True:
                c.constraint_equations.append(c.g())

    @staticmethod
    def add_constraint_damping(con):
        dom = np.dot(con.body1.A0K, con.body1.om0KK) - \
            np.dot(con.body2.A0K, con.body2.om0KK)
        M = con.damp * dom
        con.body1.add_external_force_moment(np.zeros(3), -M)
        con.body2.add_external_force_moment(np.zeros(3), M)

        if isinstance(con, constraints.PrismaticHinge):
            dv = con.body1.v0S0 - con.body2.v0S0
            F = con.damp_translational * dv
            con.body1.add_external_force_moment(-F, np.zeros(3))
            con.body2.add_external_force_moment(F, np.zeros(3))

    def update_body_states(self, t, qglobal):
        for body in self.bodies:
            body.update_state(t, qglobal)
            body.reset_external_force_moment()

    def update_body_velocities(self, qglobal):
        for body in self.bodies:
            body.update_velocities(qglobal)

    @property
    def initialize_qglobal(self):
        y = []
        z = []
        py = 0
        pz = 0
        p = 0
        for body in self.bodies:
            yb, zb = np.array_split(body.q0, 2)
            y = y + yb.tolist()
            z = z + zb.tolist()
            body.posy = py
            body.posz_rel = pz
            body.pos = p
            p = p + 1
            if type(body) is bodies.RigidBody1D:
                py += 1
                pz += 1
            else:
                py += 7
                pz += 6

        q0 = np.array(y + z)
        for body in self.bodies:
            body.posz = body.posz_rel + len(y)
        return q0

    def initialize_g(self):
        start = 0
        for c in self.constraints:
            c.pos_g = start
            start += c.dof

    @property
    def set_num_dof(self):
        numDof = 0
        for body in self.bodies:
            numDof = numDof + body.dof
        return numDof

    @property
    def assemble_mass(self):
        m = np.zeros([self.dim_z, self.dim_z])
        a1 = 0
        for body in self.bodies:
            if type(body) is bodies.RigidBody1D:
                e1 = a1 + 1
            else:
                e1 = a1 + 6

            m[a1:e1, a1:e1] = body.M

            a1 = e1
        msp = sparse.csc_matrix(m)
        mlu = sparse.linalg.factorized(msp)
        return msp

    def assemble_force(self):
        return np.zeros(self.dim_z)

    @property
    def kinematic_ode_global(self):
        a2 = 0
        yp = np.zeros(self.dim_y)
        for body in self.bodies:
            if type(body) is bodies.RigidBody1D:
                e2 = a2 + 1
            else:
                e2 = a2 + 7
            # collect kinematic equations
            yp[a2:e2] = body.kinematic_ode()
            a2 = e2
        return yp

    def kinematic_matrix_global(self):
        K = np.zeros([len(self.bodies) * 7, len(self.bodies) * 6])
        row = 0
        col = 0
        for body in self.bodies:
            K[row:row + 7, col:col + 6] = body.kinematic_matrix()
            row += 7
            col += 6
        return K

    @property
    def forces_global(self):
        b = np.zeros(self.dim_z)
        a1 = 0
        for body in self.bodies:
            if type(body) is bodies.RigidBody1D:
                e1 = a1 + 1
            else:
                e1 = a1 + 6
            # collect kinematic equations
            b[a1:e1] = body.force_moment()
            a1 = e1
        return b

    @property
    def dof_c(self):
        dof = 0
        for con in self.constraints:
            dof = dof + con.dof

        return dof

    def jacobi_constraint(self):
        num_c = len(self.constraints)
        dof_c = self.dof_c
        Jg = np.zeros([dof_c, self.dim_z])
        Jgpz = np.zeros(dof_c)
        g = np.zeros(dof_c)
        j = 0

        # Fill global Jacobian and derivation
        for con in self.constraints:
            G1, G2 = con.jacobian()
            if not isinstance(con.body1, bodies.Ground):
                pos1 = int(con.body1.pos * 6)
                Jg[j:j + con.dof, pos1:pos1 + 6] = G1

            if not isinstance(con.body2, bodies.Ground):
                pos2 = int(con.body2.pos * 6)
                Jg[j:j + con.dof, pos2:pos2 + 6] = G2

            # g[j:j + con.dof] = con.g()

            Jgpz[j:j + con.dof] = con.djacobian_z()

            j = j + con.dof
            con.g()

        return Jg, Jgpz

    def lagrange_multiplicators(self, z, Jg, Jgpz):
        T1 = sparse.csc_matrix(
            np.dot(Jg, sparse.linalg.spsolve(self.solve, Jg.transpose())))
        T2 = -Jgpz + np.dot(Jg, sparse.linalg.spsolve(self.solve, self.qe))
        la = -sparse.linalg.spsolve(T1, T2)
        mue = -sparse.linalg.spsolve(sparse.csc_matrix(
            np.dot(Jg, Jg.transpose())), np.dot(Jg, z))
        return la, mue

    def lagrange_baumgarte(self, g, gp, Jg, Jgpz):
        T1 = sparse.csc_matrix(
            np.dot(Jg, sparse.linalg.spsolve(self.solve, Jg.transpose())))
        T2 = -Jgpz + np.dot(Jg, sparse.linalg.spsolve(self.solve, self.qe))
        la = -sparse.linalg.spsolve(T1, T2 + self.alpha * gp + self.beta * g)

        return la

    def set_baumgarte(self, step_size):
        self.alpha = 1000  # 1 / step_size
        self.beta = 1500  # np.sqrt(2) / step_size

    def lagrange_lambda(self, z_global):
        Jg, Jgpz = self.jacobi_constraint()
        g = self.g_global()
        gp = np.dot(Jg, z_global)
        T1 = sparse.csc_matrix(
            np.dot(Jg, sparse.linalg.spsolve(self.solve, Jg.transpose())))
        T2 = -Jgpz + np.dot(Jg, sparse.linalg.spsolve(self.solve, self.qe))
        la = -sparse.linalg.spsolve(T1, T2)

        return la

    def g_global(self):
        g = np.zeros(self.dof_c)
        start = 0
        for c in self.constraints:
            gc = c.g()
            g[start:start + len(gc)] = gc
            start += len(gc)

        return g

    def g_global_lambda(self, y_global):
        g = np.zeros(self.dof_c)
        start = 0
        for c in self.constraints:
            if not isinstance(c.body1, bodies.Ground):
                y1 = y_global[c.body1.posy:c.body1.posy + 7]
            else:
                y1 = c.body1.q[0:7]
            if not isinstance(c.body2, bodies.Ground):
                y2 = y_global[c.body2.posy:c.body2.posy + 7]
            else:
                y2 = c.body2.q[0:7]
            g[start:start + c.dof] = c.g_lambda(y1, y2)
            start += c.dof

        return g

    @property
    def get_position_velocity(self):
        y = np.zeros(self.dim_y)
        z = np.zeros(self.dim_z)
        a1 = 0
        a2 = 0
        for body in self.bodies:
            if type(body) is bodies.RigidBody1D:
                e1 = a1 + 1
                e2 = a2 + 1
            else:
                e1 = a1 + 7
                e2 = a2 + 6
            y[a1:e1] = body.y
            z[a2:e2] = body.z
            a1 = e1
            a2 = e2
        return y, z

    def equilibrium(self):
        # Gleichgewichtslage
        qG = optimize.fsolve(self.qdot_time_fixed, self.qglobal)
        return qG

    def jacobian(self, t, q):
        epsilon = 1e-8
        func = self.qdot
        f0 = func(t, q)
        f0 = np.array(f0)
        jac = np.zeros([len(q), len(f0)])
        dx = np.zeros(len(q))
        for i in range(len(q)):
            dx[i] = epsilon
            f1 = func(t, q + dx)
            jac[i] = (np.array(f1) - f0) / (epsilon)
            dx[i] = 0.0
        return jac.transpose()

    def jacobian_mp(self, t, q):
        n_procs = 16
        func = self.qdot
        f0 = func(t, q)
        f0 = np.array(f0)
        jac = np.zeros([len(f0), len(q)])

        m = int(np.ceil(len(q) / n_procs))
        count = 0
        starts = []
        stops = []
        while count < len(q) - m:
            starts.append(count)
            stops.append(count + m)
            count = count + m

        starts.append(stops[-1])
        stops.append(len(q))
        datasets = []
        for i in range(0, n_procs):
            datasets.append((self, t, q, f0, starts[i], stops[i]))

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(jacobian_process, datasets)
            i = 0
            import ipdb
            ipdb.set_trace()
            for result in results:
                for col in result:
                    jac[:, i] = col
                    i += 1

        return jac

    def jacobian_process(self, dataset):
        g, t, q, f0, start, stop = dataset
        epsilon = 1e-8
        # jac = np.zeros([len(q), len(f0)])
        cols = []
        dx = np.zeros(len(q))
        for i in range(start, stop):
            dx[i] = epsilon
            f1 = g.qdot(t, q + dx)
            cols.append((np.array(f1) - f0) / (epsilon))
            dx[i] = 0.0
        return cols

    # def jacobian(self, x, epsilon):
    #     func = self.qdot_time_fixed
    #     x0 = np.asfarray(x)
    #     f0 = func(x0)
    #     jac = np.zeros([len(x0), len(f0)])
    #     dx = np.zeros(len(x0))
    #     for i in range(len(x0)):
    #         dx[i] = epsilon
    #         jac[i] = (func(x0 + dx) - func(x0 - dx)) / (2 * epsilon)
    #         dx[i] = 0.0
    #     return jac.transpose()

    def jacobian2(self, x, dx=10 ^ -8):
        f = self.qdot_time_fixed
        n = len(x)
        func = f(x)
        jac = np.zeros((n, n))
        for j in range(n):  # through columns to allow for vector addition
            Dxj = (abs(x[j]) * dx if x[j] != 0 else dx)
            x_plus = [(xi if k != j else xi + Dxj) for k, xi in enumerate(x)]
            jac[:, j] = (f(x_plus) - func) / Dxj
        return jac

    qdot_time_fixed = partialmethod(qdot, 0)

    def get_header(self):
        header = ['Time', 'Step']
        for mm in self.moving_marker:
            if mm.save == True:
                header.append(mm.name + '_x')
                header.append(mm.name + '_y')
                header.append(mm.name + '_z')
        for c in self.constraints:
            if c.save is True:
                data_c = c.get_constraint_force()
                for entry in data_c:
                    header.append(entry)
        for b in self.bodies:
            header += b.header(self.save_acceleration)
        for f in self.forces:
            if f.save is True:
                header.append(f.name + '_x')
                header.append(f.name + '_y')
                header.append(f.name + '_z')
                header.append(f.name + '_mx')
                header.append(f.name + '_my')
                header.append(f.name + '_mz')
        return header


class SubGroup(multiprocessing.Process, Group):
    def __init__(self, body, pipe, global_pos, solver_settings, moving_marker=[], animated_ground=[], stabilization='GGL', name='SubGroup',
                 save_acceleration=False, save_constraint_forces=False, animation_filename='animation.bin'):

        multiprocessing.Process.__init__(
            self, None, target=self.integrate, name=name)
        Group.__init__(self, [body], [], [], moving_marker=[], animated_ground=[], stabilization='GGL',
                       data_filename='data.csv', save_acceleration=False, save_constraint_forces=False, animation_filename=animation_filename)

        self.pipe = pipe
        self.global_pos = global_pos

        self.finished = False

        y = self.bodies[0].y
        z = self.bodies[0].z
        q0 = np.concatenate((y, z))
        self.qe = np.zeros(6)
        self.output_interval = solver_settings['output_interval']
        self.t_new = solver_settings['t0']
        self.r = solver.ImplicitEuler(self.qdot,
                                      t0=solver_settings['t0'],
                                      y0=q0,
                                      tend=solver_settings['tend'],
                                      step_size=solver_settings['step_size'],
                                      first_step=solver_settings['step_size'])
        # self.r = Radau(self.qdot,
        #                t0=solver_settings['t0'],
        #                y0=q0,
        #                t_bound=solver_settings['tend'],
        #                first_step=solver_settings['step_size'],
        #                jac=self.jacobian,
        #                atol=solver_settings['atol'],
        #                rtol=solver_settings['rtol'],
        #                newton_tol=solver_settings['newton_tol'],
        #                min_step=solver_settings['min_step'],
        #                max_step=solver_settings['max_step'])

    def integrate(self):
        while True:
            # Integrate
            self.r.step()

            # Send a message to inform main process that this step is finished
            self.pipe.send('Finished')

            # wait for sending final data
            msg = self.pipe.recv()

            # Send t,q and if converged to main Process
            data = {'time': self.r.t,
                    'h_rec': self.r.h_abs_rec,
                    'converged': self.r.converged,
                    'state': self.r.y}
            self.pipe.send(data)

            # Wait for response
            new_step = self.pipe.recv()
            self.r.fixed_step = new_step

    def qdot(self, t, q, update=True):
        self.update_system(t, q)
        if update:
            # Get Force
            self.pipe.send(q)
            Fext = self.pipe.recv()
            self.qe = self.bodies[0].force_moment_ext(Fext[0:3], Fext[3:6])

        # get kinematic ode
        yp_global = self.kinematic_ode_global

        # dynamic ode
        zp_global = sparse.linalg.spsolve(self.solve, self.qe)

        # state change
        qp_global = np.concatenate((yp_global, zp_global))
        # print('qp_global in qdot:', qp_global)
        return qp_global

    def update_system(self, t, qglobal):
        # Update locations of moving marker if not empty
        if self.moving_marker:
            self.update_moving_marker(t)

        # Update state of bodies
        self.update_body_states(t, qglobal)

        # get global y and z
        y_global, z_global = self.get_position_velocity
        self.y_global = y_global
        self.z_global = z_global

    def jacobian(self, t, x0):
        epsilon = 1e-8
        func = self.qdot
        f0 = func(t, x0, update=True)
        f0 = np.array(f0)
        jac = np.zeros([len(x0), len(f0)])
        dx = np.zeros(len(x0))
        for i in range(len(x0)):
            dx[i] = epsilon
            f1 = func(t, x0 + dx, update=True)
            jac[i] = (np.array(f1) - f0) / (epsilon)
            dx[i] = 0.0
        return jac.transpose()


class DataSaver:
    def __init__(self, filename, header):
        self.filename = filename
        self.header = header

        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writeheader()

    def save(self, data):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writerow(data)


class AnimationSaver:
    def __init__(self, filename):
        self.filename = filename

    def save(self, t, q, b, mm, dim_y):
        ta = np.array(t)
        qa = np.array(q)
        Y = qa[:, 0:int(dim_y)]

        for m in mm:
            if m.animation is not None:
                m.animation.position_saver.save(m.r0P0)

        with open(self.filename, 'wb') as file:
            pickle.dump(ta, file)
            pickle.dump(Y, file)
            pickle.dump(b, file)
            pickle.dump([m.animation for m in mm], file)


class Group_ALF(Group):
    def __init__(self, body, force, constraint, moving_marker=[], animated_ground=[],
                 data_filename='data.csv', save_acceleration=False, save_constraint_forces=False, animation_filename='animation.bin'):
        super().__init__(body, force, constraint, moving_marker, animated_ground, None,
                         data_filename, save_acceleration, save_constraint_forces, animation_filename)
        # self.mu, self.c, self.k = self.get_penalty()

    def qdot(self, t, qglobal):
        self.update_system(t, qglobal)

        Jg, Jgpz = self.jacobi_constraint()

        # External Forces
        self.qe = self.forces_global
        g = self.g_global()
        gp = np.dot(Jg, self.z_global)
        M = np.array(self.solve.todense())
        zpp1 = np.linalg.solve(M, self.qe)

        Ms = M + np.dot(Jg.T * self.mu, Jg)
        las = Jgpz - 2 * self.eta * gp - self.om**2 * g
        qes = np.dot(Jg.T * self.mu, las)

        Mzp = self.qe
        dzp = 1
        # Iteration:
        i = 0
        la = np.zeros(len(g))
        while dzp > 1e-6 and i < 10:
            # Calculate optimized acceleration
            zp = zpp1
            zpp1 = np.linalg.solve(Ms, Mzp + qes)
            Mzp = np.dot(M, zpp1)

            # Calculate updated Lagrange Multipliers
            gpp = np.dot(Jg, zpp1) + Jgpz
            la = la + self.mu * (gpp + 2 * self.eta * gp + self.om**2 * g)

            # Calculate acceleration change
            dzp = np.linalg.norm(np.abs(zpp1 - zp))
            i += 1
        # lasp1 = np.zeros(len(g))
        # zpp1 = np.zeros(len(self.qe))
        # H = M + np.dot(Jg.T * self.mu, Jg)
        # h = self.qe + np.dot(Jg.T * self.mu, Jgpz)
        # while dzp > 1e-8:
        #     las = lasp1
        #     zp = zpp1
        #     zpp1 = np.linalg.solve(H, h - np.dot(Jg.T, las))
        #     gpp = np.dot(Jg, zpp1) + Jgpz
        #     lasp1 = las + np.dot(self.mu, gpp)
        #     dzp = np.linalg.norm(np.abs(zpp1 - zp))

        # print(gp)

        # global constraint forces
        c_global = np.dot(Jg.T, la)

        # get kinematic ode
        yp_global = self.kinematic_ode_global

        # dynamic ode
        zp_global = zpp1
        # zp_global = np.linalg.solve(
        #     M, self.qe - np.dot(Jg.T * 6e4, g) - np.dot(Jg.T * 1e3, gp))

        # state change
        qp_global = np.concatenate((yp_global, zp_global))

        # Update constraint Forces
        for c in self.constraints:
            if c.save is True:
                c.update_constraint_force(c_global)

        if self.save_acceleration:
            for body in self.bodies:
                body.update_acceleration(qp_global)

        return qp_global

    def get_penalty(self):
        mu, damp, stiff = [], [], []
        for c in self.constraints:
            mu = np.concatenate((mu, c.mu))
            damp = np.concatenate((damp, c.c))
            stiff = np.concatenate((stiff, c.k))
        return mu, damp, stiff


class Group_DAE(Group):
    def __init__(self, body, force, constraint, moving_marker=[], animated_ground=[],
                 data_filename='data.csv', save_acceleration=False, save_constraint_forces=False, animation_filename='animation.bin',
                 t_start=0, dt_out=0.04):
        super().__init__(body, force, constraint, moving_marker, animated_ground,
                         data_filename, save_acceleration, save_constraint_forces, animation_filename)

        # Save
        self.dtout = dt_out
        self.last_save = 0
        self.qsave = [self.y_global]
        self.tsave = [t_start]

        # Initialize Q and Qd
        self.Qglobal = self.intialize_Q()
        self.Qdglobal = self.initialize_Qd()

    def residual(self, t, Q, Qd):
        # Dof part of Q
        qglobal = Q[0:self.dim_y + self.dim_z]
        self.Qglobal = Q

        # Update locations of moving marker if not empty
        if self.moving_marker:
            self.update_moving_marker(t)

        # Update state of bodies
        self.update_body_states(qglobal)

        # get global y and z
        y_global, z_global = self.get_position_velocity
        self.y_global = y_global
        self.z_global = z_global

        # Apply forces to bodies
        self.update_body_forces()

        # get global forces
        self.qe = self.forces_global

        # get global global jacobian and Lagrange-Multiplicators
        c_global = 0
        if len(self.constraints) > 0:
            Jg, la, mue = self.jacobi_lagrange_multiplicators(z_global)
            c_global = np.dot(Jg.transpose(), la)
            self.c_global = c_global

            # Update Gear-Gupta-Leimkuhler-corrected velocities
            z_global = z_global + np.dot(Jg.transpose(), mue)
            self.update_body_velocities(np.concatenate((y_global, z_global)))

            # Add constraint dampings
            for con in self.constraints:
                if isinstance(con, (constraints.Joint, constraints.Hinge, constraints.PrismaticHinge)):
                    self.add_constraint_damping(con)
            self.qe = self.forces_global

            # Update all constraint forces
            self.qe = self.qe + c_global

        # get kinematic ode
        yp_global = self.kinematic_ode_global

        # dynamic ode
        zp_global = sparse.linalg.spsolve(self.solve, self.qe)

        # state change
        qp_global = np.concatenate((yp_global, zp_global))

        # delta
        yp = Qd[0:self.dim_y]
        delta_yp = yp_global - yp

        zp = Qd[self.dim_y:self.dim_y + self.dim_z]
        delta_zp = zp_global - zp

        gp = Qd[self.dim_y + self.dim_z:]
        delta_gp = np.dot(Jg, z_global) - gp

        if t - self.last_save > self.dtout:
            # Data and animation
            self.qsave.append(self.y_global)
            self.tsave.append(t)
            self.save_animation(self.tsave, self.qsave)
            self.save_data(t, 0)
            self.last_save = t

            # constraint equation
            self.save_constraints()

        return np.concatenate((delta_yp, delta_zp, delta_gp))

    def intialize_Q(self):
        return np.concatenate((self.qglobal, np.zeros(self.gdof)))

    def initialize_Qd(self):
        return self.residual(0, self.Qglobal, np.zeros(len(self.Qglobal)))

    @property
    def gdof(self):
        gd = 0
        for c in self.constraints:
            gd += c.dof
        return gd
