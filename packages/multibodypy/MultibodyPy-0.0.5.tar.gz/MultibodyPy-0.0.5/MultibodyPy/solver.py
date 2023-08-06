import numpy as np
from scipy import sparse, optimize


class ImplicitEuler:
    def __init__(self, func, t0, y0, tend, step_size, first_step=1e-6, min_step=1e-12, max_step=1e-1, jacobian_recompute=1, jacobian_recompute_max=1, jacobian_recompute_min=1, tol=1e-6, args=()):
        self.func = func
        self.t0 = t0
        self.y0 = y0
        self.tend = tend
        self.step_size = step_size
        self.dt = step_size
        self.first_step = first_step
        self.min_step = min_step
        self.max_step = max_step

        self.args = args
        self.t = t0
        self.y = y0

        self.f = 0
        #self.jac = self.jacobian(self.y)
        self.jacobian_recompute = jacobian_recompute
        self.jacobian_recompute_max = jacobian_recompute_max
        self.jacobian_recompute_min = jacobian_recompute_min

        self.jacobi_count = 1
        self.tol = tol

        self.err = 0
        self.converged = True
        self.h_abs_rec = step_size

    def step(self):
        # print(self.jacobi_count, self.jacobian_recompute)
        # if self.jacobi_count >= self.jacobian_recompute:
        #     self.jac = self.jacobian(self.y)
        #     self.jacobi_count = 0
        # else:
        #     self.jacobi_count += 1
        self.jac = self.jacobian(self.y)
        ykp1, self.err = self.simplfied_newton()
        self.t += self.dt
        self.y = ykp1

        # Error
        # self.dt, self.jacobian_recompute = self.change_step_size(err)
        # ykp1 = scipy.optimize.newton(self.optimize_func, self.y,
        #                              maxiter=200,
        #                              tol=1e-3)

    def optimize_func(self, ykp1):
        dtp1 = self.t + self.dt
        return self.y + self.dt * self.func(dtp1, ykp1) - ykp1

    def simplfied_newton(self):
        A = np.identity(len(self.jac)) - self.dt * self.jac

        if self.args == ():
            f0 = self.func(self.t, self.y)
            f1 = self.func(self.t + self.dt, self.y)
        else:
            f0 = self.func(self.t, self.y, self.args)
            f1 = self.func(self.t + self.dt, self.y, self.args)
        dfdt = (f1 - f0) * (1. / self.dt)
        b = self.dt * f0 + self.dt * self.dt * dfdt
        dy = np.linalg.solve(A, b)
        y = self.y + dy

        err = np.linalg.norm(y - (self.y + self.dt * f0))

        return y, err

    def jacobian(self, x0):
        t = self.t
        epsilon = 1e-8
        func = self.func
        if self.args == ():
            f0 = func(t, x0, update=True)
        else:
            f0 = func(t, x0, self.args)
        f0 = np.array(f0)
        jac = np.zeros([len(x0), len(f0)])
        dx = np.zeros(len(x0))
        for i in range(len(x0)):
            dx[i] = epsilon
            if self.args == ():
                f1 = func(t, x0 + dx, update=True)
            else:
                f1 = func(t, x0 + dx, self.args)
            jac[i] = (np.array(f1) - f0) / (epsilon)
            dx[i] = 0.0
        return jac.transpose()

    def change_step_size(self, err):
        if err < self.tol:
            dt = self.dt * 1.1
            jr = self.jacobian_recompute + 1
        else:
            dt = self.dt * 0.9
            jr = self.jacobian_recompute - 100

        if dt < self.min_step:
            dt = self.min_step
        elif dt > self.max_step:
            dt = self.max_step
        else:
            dt = dt

        if jr < self.jacobian_recompute_min:
            jr = self.jacobian_recompute_min
        elif jr > self.jacobian_recompute_max:
            jr = self.jacobian_recompute_max
        else:
            jr = jr

        return dt, jr


class Trapz(ImplicitEuler):
    def __init__(self, func, t0, y0, tend, step_size, first_step=1e-6, min_step=1e-12, max_step=1e-1, jacobian_recompute=1, jacobian_recompute_max=1, jacobian_recompute_min=1, tol=1e-6, args=()):
        ImplicitEuler.__init__(self, func, t0, y0,
                               tend, step_size, first_step, min_step, max_step, jacobian_recompute, jacobian_recompute_max, jacobian_recompute_min, tol, args)

    def simplfied_newton(self):
        if self.args == ():
            f0 = self.func(self.t, self.y)
        else:
            f0 = self.func(self.t, self.y, self.args)
        f0 = np.array(f0)
        A = 2 * np.identity(len(self.jac)) / self.dt - self.jac
        b = 2 * f0
        dy = np.linalg.solve(A, b)

        y = self.y + dy

        y_low = self.y + self.dt * f0
        err = np.linalg.norm(np.abs(y - y_low))

        return y, err


class Euler_Index3:
    def __init__(self, group, t0, tend, step_size, first_step=1e-6, err=1e-6, maxiter=50):
        self.group = group
        self.t0 = t0
        self.tend = tend
        self.step_size = step_size
        self.first_step = first_step
        self.h = first_step
        self.err = err
        self.maxiter = maxiter

        self.t = t0
        self.q = group.qglobal
        self.y = group.qglobal[0:self.group.dim_y]
        self.z = group.qglobal[self.group.dim_y:]

        self.la = group.lagrange_lambda(self.z)

    def step(self):
        # Update Group
        self.t += self.h
        self.group.update_system(self.t, self.q)

        # Paramters
        self.K = self.group.kinematic_matrix_global()

        # Update Lambda with Newton Raphson
        self.Jg, Jgpz = self.group.jacobi_constraint()
        M = self.group.solve
        # self.la = self.optimize_lambda()
        self.la = optimize.newton_krylov(self.nonlinear_constraint,
                                         self.la,
                                         f_tol=1e-12)
        # self.la = sol.x
        # print(sol.nit)

        # External Forces
        self.group.update_body_forces()
        qe = self.group.forces_global

        # Constraint Forces
        qz = np.dot(self.Jg.T, self.la)

        # integrate dynamic ODE
        z = self.z + self.h * sparse.linalg.spsolve(M, qe + qz)

        # integrate kinematic ODE
        y = self.y + self.h * np.dot(self.K, z)

        # Update states
        self.y = y
        self.z = z
        self.q = np.concatenate((self.y, self.z))
        self.h = self.step_size

        # Update constraint Forces
        for c in self.group.constraints:
            if c.save is True:
                c.update_constraint_force(qz)

        return self.t, self.q

    def optimize_lambda(self):
        Jg = self.Jg
        M = self.group.solve
        dgdla = self.h**2 * np.dot(Jg, sparse.linalg.spsolve(M, Jg.T))
        la = self.la
        dla = 2 * self.err
        i = 0
        while np.linalg.norm(dla) > self.err and i < self.maxiter:
            # for i in range(0, 3):
            gla = self.nonlinear_constraint(la)
            dla = np.linalg.solve(dgdla, -gla)

            la += dla
        return la

    def nonlinear_constraint(self, la):
        K = self.K
        y = self.y
        z = self.z
        h = self.h
        M = self.group.solve
        qe = self.group.forces_global
        Jg = self.Jg
        yd = np.dot(K, z + h * sparse.linalg.spsolve(M, qe + np.dot(Jg.T, la)))
        yp1 = y + h * yd

        self.group.update_body_states(self.t, np.concatenate((yp1, z)))

        return self.group.g_global()


class Euler:
    def __init__(self, func, t0, y0, tend, step_size):
        self.func = func
        self.t0 = t0
        self.y0 = y0
        self.tend = tend
        self.step_size = step_size

        self.y = y0
        self.t = t0

    def step(self):
        # Parameter
        h = self.step_size
        t = self.t
        y = self.y

        S = self.func(t, y)

        self.y = y + h * S
        self.t = t + h


class Heun:
    def __init__(self, func, t0, y0, tend, step_size):
        self.func = func
        self.t0 = t0
        self.y0 = y0
        self.tend = tend
        self.step_size = step_size

        self.y = y0
        self.t = t0

    def step(self):
        # Parameter
        h = self.step_size
        t = self.t
        y = self.y

        K1 = self.func(t, y)

        y2 = y + h * K1
        K2 = self.func(t + h, y2)

        S = 1 / 2 * (K1 + K2)

        self.y = y + h * S
        self.t = t + h


class RK4:
    def __init__(self, func, t0, y0, tend, step_size):
        self.func = func
        self.t0 = t0
        self.y0 = y0
        self.tend = tend
        self.step_size = step_size

        self.y = y0
        self.t = t0

    def step(self):
        # Parameter
        h = self.step_size
        t = self.t
        y = self.y

        K1 = self.func(t, y)

        y2 = y + h / 2 * K1
        K2 = self.func(t + h / 2, y2)

        y3 = y + h / 2 * K2
        K3 = self.func(t + h / 2, y3)

        y4 = y + h * K3
        K4 = self.func(t + h, y4)

        S = 1 / 6 * (K1 + 2 * K2 + 2 * K3 + K4)

        self.y = y + h * S
        self.t = t + h


class RadauIIA3(ImplicitEuler):
    def __init__(self, func, t0, y0, tend, step_size):
        super().__init__(func, t0, y0, tend, step_size)

        self.y = y0
        self.t = t0

        self.A = np.array([[5 / 12, -1 / 12],
                           [3 / 4, 1 / 4]])
        self.b = [3 / 4, 1 / 4]
        self.c = [1 / 3, 1]
        self.d = np.dot(self.b, np.linalg.inv(self.A))

    def simplfied_newton(self):
        # Parameter
        stage = 2
        h = self.step_size
        t = self.t
        y = self.y
        A = self.A
        b = self.b
        c = self.c
        d = self.d
        J = self.jac

        Z = np.zeros(stage * len(y))
        I = np.identity(len(J))
        M1 = I - h * A[0, 0] * J
        M2 = -h * A[0, 1] * J
        M3 = -h * A[1, 0] * J
        M4 = I - h * A[1, 1] * J
        IhAJ = np.block([[M1, M2],
                         [M3, M4]])

        M1 = A[0, 0] * I
        M2 = A[0, 1] * I
        M3 = A[1, 0] * I
        M4 = A[1, 1] * I
        AI = np.block([[M1, M2],
                       [M3, M4]])

        # Iteration
        dZ = np.ones(len(Z))
        eta = 1
        i = 0
        for i in range(0, 1):
            f0 = self.func(t + c[0] * h, y + Z[0:len(y)])
            f1 = self.func(t + c[1] * h, y + Z[len(y):])
            F = np.concatenate((f0, f1))
            r = -Z + h * np.dot(AI, F)
            dZp1 = np.linalg.solve(IhAJ, r)
            Z = Z + dZp1
            dZ = dZp1
            i += 1

        dz = np.zeros(len(y))
        for i in range(0, stage):
            dz = dz + d[i] * Z[i]

        y = y + dz

        #y = self.y + h * self.func(t, self.y)

        return y, 0


class RadauIIA5(ImplicitEuler):
    def __init__(self, func, t0, y0, tend, step_size):
        super().__init__(func, t0, y0, tend, step_size)

        self.y = y0
        self.t = t0

        self.A = np.array([[(88 - 7 * np.sqrt(6)) / 360,
                            (296 - 169 * np.sqrt(6)) / 1800,
                            (-2 + 3 * np.sqrt(6)) / 225],
                           [(296 + 169 * np.sqrt(6)) / 1800,
                            (88 + 7 * np.sqrt(6)) / 360,
                            (-2 - 3 * np.sqrt(6)) / 225],
                           [(16 - np.sqrt(6)) / 36,
                            (16 + np.sqrt(6)) / 36,
                            1 / 9]])
        self.b = [(16 - np.sqrt(6)) / 36,
                  (16 + np.sqrt(6)) / 36,
                  1 / 9]
        self.c = [(4 - np.sqrt(6)) / 10,
                  (4 + np.sqrt(6)) / 10,
                  1]
        self.d = np.linalg.solve(self.A, self.b)

    def simplfied_newton(self):
        # Parameter
        stage = 3
        h = self.step_size
        t = self.t
        y = self.y
        A = self.A
        b = self.b
        c = self.c
        d = self.d
        J = self.jac

        Z = np.zeros(stage * len(y))
        I = np.identity(len(J))
        M = []
        for i in range(0, stage):
            for j in range(0, stage):
                if j == 0:
                    M.append(I - h * A[i, j] * J)
                else:
                    M.append(-h * A[i, j] * J)
        IhAJ = np.block([[M[0], M[1], M[2]],
                         [M[3], M[4], M[5]],
                         [M[6], M[7], M[8]]])
        M = []
        for i in range(0, stage):
            for j in range(0, stage):
                M.append(A[i, j] * I)
        AI = np.block([[M[0], M[1], M[2]],
                       [M[3], M[4], M[5]],
                       [M[6], M[7], M[8]]])
        import ipdb
        ipdb.set_trace()
        # Iteration
        dZ = np.ones(len(Z))
        eta = 1
        i = 0
        for i in range(0, 20):
            f0 = self.func(t + c[0] * h, y + Z[0:len(y)])
            f1 = self.func(t + c[1] * h, y + Z[len(y):2 * len(y)])
            f2 = self.func(t + c[2] * h, y + Z[2 * len(y):])
            F = np.concatenate((f0, f1, f2))
            r = -Z + h * np.dot(AI, F)
            dZp1 = np.linalg.solve(IhAJ, r)
            Z = Z + dZp1
            dZ = dZp1
            print(Z)
            i += 1

        dz = np.zeros(len(y))
        for i in range(0, stage):
            dz = dz + d[i] * Z[i]

        y = y + dz

        #y = self.y + h * self.func(t, self.y)

        return y, 0
