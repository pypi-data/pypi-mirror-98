import numpy as np
from MultibodyPy import bodies


def cross(a, b):
    c = [a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0]]

    return np.array(c)


class Constraint:
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, save=False):
        self.p1 = p1
        self.p2 = p2

        self.body1 = p1.body
        self.body2 = p2.body

        self.save = save
        if self.save == True:
            self.constraint_equations = []

        self.posg = 0

    def g(self):
        pass

    def jacobian(self):
        pass

    def djacobian_z(self):
        pass

    @staticmethod
    def tilde(vec):
        return np.array([[0, -vec[2], vec[1]], [vec[2], 0, -vec[0]], [-vec[1], vec[0], 0]])

    @staticmethod
    def get_perpendicular_axis(axis):
        ex = np.array([1, 0, 0])
        ey = np.array([0, 1, 0])
        m2 = np.dot(Constraint.tilde(axis), ex)
        if np.dot(m2.T, m2) == 0:
            m2 = np.abs(np.dot(Constraint.tilde(axis), ey))

        n2 = np.abs(np.dot(Constraint.tilde(axis), m2))
        return m2, n2

    @staticmethod
    def rotation_matrix(pE):
        e0, e1, e2, e3 = pE
        G = np.array(
            [[-e1, e0, -e3, e2], [-e2, e3, e0, -e1], [-e3, -e2, e1, e0]])
        L = np.array(
            [[-e1, e0, e3, -e2], [-e2, -e3, e0, e1], [-e3, e2, -e1, e0]])
        A0K = np.dot(G, L.transpose())
        return A0K, G, L


class Joint(Constraint):
    dof = 3

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, rotational_damping=0, save=False, name='Joint'):
        Constraint.__init__(self, p1, p2, save)
        self.damp = rotational_damping
        self.qz = np.zeros(self.dof)
        self.name = name

    def update_constraint_force(self, c_global):
        self.qz = c_global[self.body1.posz_rel:self.body1.posz_rel + 3]

    def get_constraint_force(self):
        data = {
            f'{self.name}_Fg1': self.qz[0],
            f'{self.name}_Fg2': self.qz[1],
            f'{self.name}_Fg3': self.qz[2],
        }
        return data

    def g(self):
        gy = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        # print(gy)
        return gy

    def g_lambda(self, y1, y2):
        # Location and Euler Parameter
        r010 = y1[0:3]
        pE1 = y1[3:7]
        r020 = y2[0:3]
        pE2 = y2[3:7]

        # Rotation matrices
        A01, _, _ = self.rotation_matrix(pE1)
        A02, _, _ = self.rotation_matrix(pE2)

        # Constraint equation
        gy = r020 + np.dot(A02, self.p2.rSPK) - \
            (r010 + np.dot(A01, self.p1.rSPK))

        return gy

    def jacobian(self):
        Jg1 = np.zeros([3, 6])
        Jg2 = np.zeros([3, 6])
        E = np.identity(3)

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        Jg1[:, 0:3] = E
        Jg1[:, 3:6] = np.dot(self.body1.A0K, bodies.tilde(r1B1).transpose())
        Jg2[:, 0:3] = -E
        Jg2[:, 3:6] = -np.dot(self.body2.A0K, bodies.tilde(r2B2).transpose())
        return Jg1, Jg2

    def djacobian_z(self):
        om1 = self.body1.om0KK
        om2 = self.body2.om0KK
        return np.dot(self.body2.A0K, (cross(om2, cross(om2, self.p2.rSPK)))) - np.dot(self.body1.A0K, (
            cross(om1, cross(om1, self.p1.rSPK))))


class Joint_move(Constraint):
    dof = 3

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, rotational_damping=0, save=False, name='Joint'):
        Constraint.__init__(self, p1, p2, save)
        self.damp = rotational_damping
        self.qz = np.zeros(3)
        self.name = name

    def update_constraint_force(self, c_global):
        self.qz = c_global[self.body1.posz_rel:self.body1.posz_rel + 3]

    def get_constraint_force(self):
        data = {
            f'{self.name}_Fg1': self.qz[0],
            f'{self.name}_Fg2': self.qz[1],
            f'{self.name}_Fg3': self.qz[2],
        }
        return data

    def g(self):
        gy = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        # print(gy)
        return gy

    def g_lambda(self, y1, y2):
        # Location and Euler Parameter
        r010 = y1[0:3]
        pE1 = y1[3:7]
        r020 = y2[0:3]
        pE2 = y2[3:7]

        # Rotation matrices
        A01, _, _ = self.rotation_matrix(pE1)
        A02, _, _ = self.rotation_matrix(pE2)

        # Constraint equation
        gy = r020 + np.dot(A02, self.p2.rSPK) - \
            (r010 + np.dot(A01, self.p1.rSPK))

        return gy

    def jacobian(self):
        Jg1 = np.zeros([3, 6])
        Jg2 = np.zeros([3, 6])
        E = np.identity(3)

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        Jg1[:, 0:3] = E
        Jg1[:, 3:6] = np.dot(self.body1.A0K, bodies.tilde(r1B1).transpose())
        Jg2[:, 0:3] = -E
        Jg2[:, 3:6] = -np.dot(self.body2.A0K,
                              bodies.tilde(r2B2).transpose())

        return Jg1, Jg2

    def djacobian_z(self):
        om1 = self.body1.om0KK
        om2 = self.body2.om0KK
        return np.dot(self.body2.A0K, (cross(om2, cross(om2, self.p2.rSPK)))) - np.dot(self.body1.A0K, (
            cross(om1, cross(om1, self.p1.rSPK))))


class Hinge(Constraint):
    dof = 5

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, axis_body: bodies.RigidBody,
                 rotational_damping=0, name="Hinge", save=False):
        Constraint.__init__(self, p1, p2, save)
        self.rotation_axis = np.array(axis)

        self.axis_body = axis_body

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.m2, self.n2 = self.get_perpendicular_axis(self.rotation_axis)

        self.damp = rotational_damping

        self.name = name

        self.Jg1 = np.array([[1, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

        self.Jg2 = np.array([[-1, 0, 0, 0, 0, 0],
                             [0, -1, 0, 0, 0, 0],
                             [0, 0, -1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

        self.qz = np.zeros(self.dof)

    def update_constraint_force(self, c_global):
        self.qz = c_global[self.body1.posz_rel:self.body1.posz_rel + self.dof]

    def get_constraint_force(self):
        data = {
            f'{self.name}_Fg1': self.qz[0],
            f'{self.name}_Fg2': self.qz[1],
            f'{self.name}_Fg3': self.qz[2],
            f'{self.name}_Fg4': self.qz[3],
            f'{self.name}_Fg5': self.qz[4],
        }
        return data

    def g(self):
        # Axis for rotational constraints
        s = np.dot(self.body1.A0K, self.ey)
        a = np.dot(self.body2.A0K, self.ex)
        b = np.dot(self.body2.A0K, self.ez)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        # Constraint equations
        gy1 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        gy2 = np.dot(np.dot(A12, m2.T).T, u2)
        gy3 = np.dot(np.dot(A12, n2.T).T, u2)
        return np.hstack((gy1, gy2, gy3))

    def g_lambda(self, y1, y2):
        # Location and Euler Parameter
        r010 = y1[0:3]
        pE1 = y1[3:7]
        r020 = y2[0:3]
        pE2 = y2[3:7]

        # Rotation matrices
        A01, _, _ = self.rotation_matrix(pE1)
        A02, _, _ = self.rotation_matrix(pE2)
        A12 = np.dot(A01.T, A02)

        # Axis for rotational constraints
        s = np.dot(A01, self.ey)
        a = np.dot(A02, self.ex)
        b = np.dot(A02, self.ez)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # Constraint equations
        gy1 = r020 + np.dot(A02, self.p2.rSPK) - \
            (r010 + np.dot(A01, self.p1.rSPK))
        gy2 = np.dot(np.dot(A12, m2.T).T, u2)
        gy3 = np.dot(np.dot(A12, n2.T).T, u2)
        return np.hstack((gy1, gy2, gy3))

    def jacobian(self):
        E = np.identity(3)
        Z1 = np.zeros([1, 3])

        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        # self.Jg1[0:3, 3:] = np.dot(A01, bodies.tilde(r1B1).T)
        # self.Jg1[3, 3:] = -np.dot(self.tilde(m2).T, u2)
        # self.Jg1[4, 3:] = -np.dot(self.tilde(n2).T, u2)
        #
        # self.Jg2[0:3, 3:] = -np.dot(A02, bodies.tilde(r2B2).T)
        # self.Jg2[3, 3:] = np.dot(A12.T, np.dot(self.tilde(m2).T, u2))
        # self.Jg2[4, 3:] = np.dot(A12.T, np.dot(self.tilde(n2).T, u2))

        Jg1 = np.block([[E, np.dot(A01, bodies.tilde(r1B1).T)],
                        [Z1, -np.dot(self.tilde(m2).T, u2)],
                        [Z1, -np.dot(self.tilde(n2).T, u2)]])

        Jg2 = np.block([[-E, -np.dot(A02, bodies.tilde(r2B2).T)],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(m2).T, u2))],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(n2).T, u2))]])

        return Jg1, Jg2

    def djacobian_z(self):
        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        u2 = self.rotation_axis
        m2 = self.m2
        n2 = self.n2

        om1 = self.body1.om0KK
        om2 = self.body2.om0KK

        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        A01d = self.body1.derivation_rotation_matrix
        A02d = self.body2.derivation_rotation_matrix
        A12dT = np.dot(A01d.transpose(), A02) + np.dot(A01.transpose(), A02d)

        Jgpz = np.block([-np.dot(A01d, np.dot(self.tilde(r1B1).T, om1)) + np.dot(A02d, np.dot(self.tilde(r2B2).T, om2)),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(m2).T, u2)), om2),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(n2).T, u2)), om2)])

        return Jgpz


class Hinge_reduced(Constraint):
    dof = 3

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, axis_body: bodies.RigidBody,
                 rotational_damping=0, name="Hinge", save=False):
        Constraint.__init__(self, p1, p2, save)
        self.rotation_axis = np.array(axis)

        self.axis_body = axis_body

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.m2, self.n2 = self.get_perpendicular_axis(self.rotation_axis)

        self.damp = rotational_damping

        self.name = name

        self.Jg1 = np.array([[1, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

        self.Jg2 = np.array([[-1, 0, 0, 0, 0, 0],
                             [0, -1, 0, 0, 0, 0],
                             [0, 0, -1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

        self.qz = np.zeros(3)

    def update_constraint_force(self, c_global):
        self.qz = c_global[self.body1.posz_rel:self.body1.posz_rel + 3]

    def get_constraint_force(self):
        data = {
            f'{self.name}_Fg1': self.qz[0],
            f'{self.name}_Fg2': self.qz[1],
            f'{self.name}_Fg3': self.qz[2],
        }
        return data

    def g(self):
        # Axis for rotational constraints
        s = np.dot(self.body1.A0K, self.ey)
        a = np.dot(self.body2.A0K, self.ex)
        b = np.dot(self.body2.A0K, self.ez)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        # Constraint equations
        gy1 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        gy2 = np.dot(np.dot(A12, m2.T).T, u2)
        gy3 = np.dot(np.dot(A12, n2.T).T, u2)
        return np.hstack((gy1, gy2, gy3))

    def g_lambda(self, y1, y2):
        # Location and Euler Parameter
        r010 = y1[0:3]
        pE1 = y1[3:7]
        r020 = y2[0:3]
        pE2 = y2[3:7]

        # Rotation matrices
        A01, _, _ = self.rotation_matrix(pE1)
        A02, _, _ = self.rotation_matrix(pE2)
        A12 = np.dot(A01.T, A02)

        # Axis for rotational constraints
        s = np.dot(A01, self.ey)
        a = np.dot(A02, self.ex)
        b = np.dot(A02, self.ez)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # Constraint equations
        gy1 = r020 + np.dot(A02, self.p2.rSPK) - \
            (r010 + np.dot(A01, self.p1.rSPK))
        gy2 = np.dot(np.dot(A12, m2.T).T, u2)
        gy3 = np.dot(np.dot(A12, n2.T).T, u2)
        return np.hstack((gy1, gy2, gy3))

    def jacobian(self):
        E = np.identity(3)
        Z1 = np.zeros([1, 3])

        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        # self.Jg1[0:3, 3:] = np.dot(A01, bodies.tilde(r1B1).T)
        # self.Jg1[3, 3:] = -np.dot(self.tilde(m2).T, u2)
        # self.Jg1[4, 3:] = -np.dot(self.tilde(n2).T, u2)
        #
        # self.Jg2[0:3, 3:] = -np.dot(A02, bodies.tilde(r2B2).T)
        # self.Jg2[3, 3:] = np.dot(A12.T, np.dot(self.tilde(m2).T, u2))
        # self.Jg2[4, 3:] = np.dot(A12.T, np.dot(self.tilde(n2).T, u2))

        Jg1 = np.block([[E, np.dot(A01, bodies.tilde(r1B1).T)],
                        [Z1, -np.dot(self.tilde(m2).T, u2)],
                        [Z1, -np.dot(self.tilde(n2).T, u2)]])

        Jg2 = np.block([[-E, -np.dot(A02, bodies.tilde(r2B2).T)],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(m2).T, u2))],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(n2).T, u2))]])

        Jg1 = np.delete(Jg1, [2, 4], 0)
        Jg2 = np.delete(Jg2, [2, 4], 0)
        return Jg1, Jg2

    def djacobian_z(self):
        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        u2 = self.rotation_axis
        m2 = self.m2
        n2 = self.n2

        om1 = self.body1.om0KK
        om2 = self.body2.om0KK

        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        A01d = self.body1.derivation_rotation_matrix
        A02d = self.body2.derivation_rotation_matrix
        A12dT = np.dot(A01d.transpose(), A02) + np.dot(A01.transpose(), A02d)

        Jgpz = np.block([-np.dot(A01d, np.dot(self.tilde(r1B1).T, om1)) + np.dot(A02d, np.dot(self.tilde(r2B2).T, om2)),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(m2).T, u2)), om2),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(n2).T, u2)), om2)])
        Jgpz = np.delete(Jgpz, [2, 4], 0)
        return Jgpz


class Fixed(Constraint):
    dof = 6

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, name="Fix", save=False):
        Constraint.__init__(self, p1, p2, save)

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.name = name

        self.Jg1 = np.array([[1, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

        self.Jg2 = np.array([[-1, 0, 0, 0, 0, 0],
                             [0, -1, 0, 0, 0, 0],
                             [0, 0, -1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]])

    def jacobian(self):
        E = np.identity(3)
        Z1 = np.zeros([1, 3])

        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        # self.Jg1[0:3, 3:] = np.dot(A01, bodies.tilde(r1B1).T)
        # self.Jg1[3, 3:] = -np.dot(self.tilde(m2).T, u2)
        # self.Jg1[4, 3:] = -np.dot(self.tilde(n2).T, u2)
        #
        # self.Jg2[0:3, 3:] = -np.dot(A02, bodies.tilde(r2B2).T)
        # self.Jg2[3, 3:] = np.dot(A12.T, np.dot(self.tilde(m2).T, u2))
        # self.Jg2[4, 3:] = np.dot(A12.T, np.dot(self.tilde(n2).T, u2))

        Jg1 = np.block([[E, np.dot(A01, bodies.tilde(r1B1).T)],
                        [Z1, -np.dot(self.tilde(m2).T, u2)],
                        [Z1, -np.dot(self.tilde(n2).T, u2)]])

        Jg2 = np.block([[-E, -np.dot(A02, bodies.tilde(r2B2).T)],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(m2).T, u2))],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(n2).T, u2))]])

        return Jg1, Jg2

    def djacobian_z(self):
        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        u2 = self.rotation_axis
        m2 = self.m2
        n2 = self.n2

        om1 = self.body1.om0KK
        om2 = self.body2.om0KK

        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        A01d = self.body1.derivation_rotation_matrix
        A02d = self.body2.derivation_rotation_matrix
        A12dT = np.dot(A01d.transpose(), A02) + np.dot(A01.transpose(), A02d)

        Jgpz = np.block([-np.dot(A01d, np.dot(self.tilde(r1B1).T, om1)) + np.dot(A02d, np.dot(self.tilde(r2B2).T, om2)),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(m2).T, u2)), om2),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(n2).T, u2)), om2)])

        return Jgpz


class Joint_reduced(Constraint):
    dof = 2

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, rotational_damping=0, save=False, name='Joint'):
        Constraint.__init__(self, p1, p2, save)
        self.damp = rotational_damping
        self.qz = np.zeros(self.dof)
        self.name = name

    def update_constraint_force(self, c_global):
        self.qz = c_global[self.posg:self.posg + self.dof]

    def get_constraint_force(self):
        data = {
            f'{self.name}_Fg1': self.qz[0],
            f'{self.name}_Fg2': self.qz[1]
        }
        return data

    def g(self):
        gy = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        return [gy[0], gy[1]]

    def g_lambda(self, y1, y2):
        # Location and Euler Parameter
        r010 = y1[0:3]
        pE1 = y1[3:7]
        r020 = y2[0:3]
        pE2 = y2[3:7]

        # Rotation matrices
        A01, _, _ = self.rotation_matrix(pE1)
        A02, _, _ = self.rotation_matrix(pE2)

        # Constraint equation
        gy = r020 + np.dot(A02, self.p2.rSPK) - \
            (r010 + np.dot(A01, self.p1.rSPK))

        return gy

    def jacobian(self):
        Jg1 = np.zeros([3, 6])
        Jg2 = np.zeros([3, 6])
        E = np.identity(3)

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK
        r2B2 = self.p2.rSPK

        Jg1[:, 0:3] = E
        Jg1[:, 3:6] = np.dot(self.body1.A0K, bodies.tilde(r1B1).transpose())
        Jg2[:, 0:3] = -E
        Jg2[:, 3:6] = -np.dot(self.body2.A0K, bodies.tilde(r2B2).transpose())

        Jg1 = np.delete(Jg1, 1, 0)
        Jg2 = np.delete(Jg2, 1, 0)

        return Jg1, Jg2

    def djacobian_z(self):
        om1 = self.body1.om0KK
        om2 = self.body2.om0KK
        Jgpz = np.dot(self.body2.A0K, (cross(om2, cross(om2, self.p2.rSPK)))) - \
            np.dot(self.body1.A0K, (cross(om1, cross(om1, self.p1.rSPK))))

        Jgpz = np.delete(Jgpz, 1, 0)

        return Jgpz


class Prismatic(Constraint):
    dof = 5

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, damp=0, name="Prismatic", save=False):
        Constraint.__init__(self, p1, p2, save)
        self.slide_axis = np.array(axis)

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.p11, self.p21 = self.get_perpendicular_axis(self.slide_axis)

        # Initial Connection Array
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        r1P11 = self.p1.rSPK
        r2P22 = self.p2.rSPK
        r0P10 = self.body1.r0S0 + np.dot(A01, r1P11)
        r0P20 = self.body2.r0S0 + np.dot(A02, r2P22)
        self.r0 = r0P20 - r0P10

        self.damp = damp

        self.name = name

        self.Jg1 = np.zeros([5, 6])
        self.Jg2 = np.zeros([5, 6])
        self.qz = np.zeros(5)

    def update_constraint_force(self, c_global):
        self.qz = c_global[self.body1.posz_rel:self.body1.posz_rel + self.dof]

    def get_constraint_force(self):
        data = {
            f'{self.name}_Fg1': self.qz[0],
            f'{self.name}_Fg2': self.qz[1],
            f'{self.name}_Fg3': self.qz[2],
            f'{self.name}_Fg4': self.qz[3],
            f'{self.name}_Fg5': self.qz[4],
        }
        return data

    def g(self):
        # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r1P11 = self.p1.rSPK
        r2P22 = self.p2.rSPK
        r0P10 = self.body1.r0S0 + np.dot(A01, r1P11)
        r0P20 = self.body2.r0S0 + np.dot(A02, r2P22)
        rP1P20 = r0P20 - r0P10 - self.r0

        # Two connection constraints
        g1 = np.dot(p10.T, rP1P20)
        g2 = np.dot(p20.T, rP1P20)

        # 3 Perpendicular constraints
        g3 = np.dot(ex10.T, ey20)
        g4 = np.dot(ey10.T, ez20)
        g5 = np.dot(ez10.T, ex20)

        return [g1, g2, g3, g4, g5]

    def jacobian(self):
        # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r120 = self.body2.r0S0 - self.body1.r0S0

        # Two connection constraints
        self.Jg1[0, 0:3] = -p10.T
        self.Jg1[0, 3:6] = -np.dot(r120.T, np.dot(self.tilde(p10), A01))
        self.Jg1[1, 0:3] = -p20.T
        self.Jg1[1, 3:6] = -np.dot(r120.T, np.dot(self.tilde(p20), A01))

        self.Jg2[0, 0:3] = p10.T
        self.Jg2[1, 0:3] = p20.T

        # Three perpendicular constraints
        self.Jg1[2, 3:6] = -np.dot(ey20.T, np.dot(self.tilde(ex10), A01))
        self.Jg1[3, 3:6] = -np.dot(ez20.T, np.dot(self.tilde(ey10), A01))
        self.Jg1[4, 3:6] = -np.dot(ex20.T, np.dot(self.tilde(ez10), A01))

        self.Jg2[2, 3:6] = -np.dot(ex10.T, np.dot(self.tilde(ey20), A02))
        self.Jg2[3, 3:6] = -np.dot(ey10.T, np.dot(self.tilde(ez20), A02))
        self.Jg2[4, 3:6] = -np.dot(ez10.T, np.dot(self.tilde(ex20), A02))

        return self.Jg1, self.Jg2

    def djacobian_z(self):
         # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r120 = self.body2.r0S0 - self.body1.r0S0

        # Derivative of rotation matrix
        A01d = self.body1.A0Kd
        A02d = self.body2.A0Kd

        # Derivative of global perpendicular arrays
        p10d = np.dot(A01d, self.p11)
        p20d = np.dot(A01d, self.p21)

        # Derivative of global unit arrays
        ex10d = np.dot(A01d, self.ex)
        ey10d = np.dot(A01d, self.ey)
        ez10d = np.dot(A01d, self.ez)
        ex20d = np.dot(A02d, self.ex)
        ey20d = np.dot(A02d, self.ey)
        ez20d = np.dot(A02d, self.ez)

        # Derivative of connection array
        r120d = self.body2.v0S0 - self.body1.v0S0

        # Global angular velocities
        om010 = np.dot(A01, self.body1.om0KK)
        om020 = np.dot(A02, self.body2.om0KK)

        # Jgp*z
        Jgpz = np.zeros(5)
        Jgpz[0] = - np.dot(p10.T, np.dot(self.tilde(om010), r120d)) \
            - np.dot(r120.T, np.dot(self.tilde(om010), p10d)) \
            - 2 * np.dot(r120d.T, p10d)
        Jgpz[1] = - np.dot(p20.T, np.dot(self.tilde(om010), r120d)) \
            - np.dot(r120.T, np.dot(self.tilde(om010), p20d)) \
            - 2 * np.dot(r120d.T, p20d)
        Jgpz[2] = - np.dot(ex10.T, np.dot(self.tilde(om020), ey20d)) \
            - np.dot(ey20.T, np.dot(self.tilde(om010), ex10d)) \
            - 2 * np.dot(ey20d.T, ex10d)
        Jgpz[3] = - np.dot(ey10.T, np.dot(self.tilde(om020), ez20d)) \
            - np.dot(ez20.T, np.dot(self.tilde(om010), ey10d)) \
            - 2 * np.dot(ez20d.T, ey10d)
        Jgpz[4] = - np.dot(ez10.T, np.dot(self.tilde(om020), ex20d)) \
            - np.dot(ex20.T, np.dot(self.tilde(om010), ez10d)) \
            - 2 * np.dot(ex20d.T, ez10d)

        return Jgpz


class PrismaticHinge(Constraint):
    dof = 4

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, damp=0, name="PrismaticHinge", save=False, penalty_factors=[1, 1, 1]):
        Constraint.__init__(self, p1, p2, save)
        self.slide_axis = np.array(axis)
        #self.rotation_axis = np.array(rotation_axis)

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.p11, self.p21 = self.get_perpendicular_axis(self.slide_axis)

        # Initial Connection Array
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        r1P11 = self.p1.rSPK
        r2P22 = self.p2.rSPK
        r0P10 = self.body1.r0S0 + np.dot(A01, r1P11)
        r0P20 = self.body2.r0S0 + np.dot(A02, r2P22)
        self.r0 = r0P20 - r0P10

        self.damp = damp

        self.name = name

        self.Jg1 = np.zeros([4, 6])
        self.Jg2 = np.zeros([4, 6])

        # Penalty Factors for Augmented Lagrange Formulation for this constraint
        mu = penalty_factors[0]
        c = penalty_factors[1]
        k = penalty_factors[2]
        print(f'eta={0.5 * c / mu}')
        print(f'om={np.sqrt(k / mu)}')
        self.mu = np.ones(self.dof) * penalty_factors[0]
        self.c = np.ones(self.dof) * penalty_factors[1]
        self.k = np.ones(self.dof) * penalty_factors[2]

    def g(self):
        # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r1P11 = self.p1.rSPK
        r2P22 = self.p2.rSPK
        r0P10 = self.body1.r0S0 + np.dot(A01, r1P11)
        r0P20 = self.body2.r0S0 + np.dot(A02, r2P22)
        rP1P20 = r0P20 - r0P10

        # Two connection constraints
        g1 = np.dot(p10.T, rP1P20)
        g2 = np.dot(p20.T, rP1P20)

        # Two Perpendicular constraints
        #g3 = np.dot(ex10.T, ey20)
        g4 = np.dot(ey10.T, ez20)
        g5 = np.dot(ez10.T, ex20)

        return [g1, g2, g4, g5]

    def jacobian(self):
        # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r120 = self.body2.r0S0 - self.body1.r0S0

        # Two connection constraints
        self.Jg1[0, 0:3] = -p10.T
        self.Jg1[0, 3:6] = -np.dot(r120.T, np.dot(self.tilde(p10), A01))
        self.Jg1[1, 0:3] = -p20.T
        self.Jg1[1, 3:6] = -np.dot(r120.T, np.dot(self.tilde(p20), A01))

        self.Jg2[0, 0:3] = p10.T
        self.Jg2[1, 0:3] = p20.T

        # Three perpendicular constraints
        #self.Jg1[2, 3:6] = -np.dot(ey20.T, np.dot(self.tilde(ex10), A01))
        self.Jg1[2, 3:6] = -np.dot(ez20.T, np.dot(self.tilde(ey10), A01))
        self.Jg1[3, 3:6] = -np.dot(ex20.T, np.dot(self.tilde(ez10), A01))

        #self.Jg2[2, 3:6] = -np.dot(ex10.T, np.dot(self.tilde(ey20), A02))
        self.Jg2[2, 3:6] = -np.dot(ey10.T, np.dot(self.tilde(ez20), A02))
        self.Jg2[3, 3:6] = -np.dot(ez10.T, np.dot(self.tilde(ex20), A02))

        return self.Jg1, self.Jg2

    def djacobian_z(self):
         # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r120 = self.body2.r0S0 - self.body1.r0S0

        # Derivative of rotation matrix
        A01d = self.body1.A0Kd
        A02d = self.body2.A0Kd

        # Derivative of global perpendicular arrays
        p10d = np.dot(A01d, self.p11)
        p20d = np.dot(A01d, self.p21)

        # Derivative of global unit arrays
        ex10d = np.dot(A01d, self.ex)
        ey10d = np.dot(A01d, self.ey)
        ez10d = np.dot(A01d, self.ez)
        ex20d = np.dot(A02d, self.ex)
        ey20d = np.dot(A02d, self.ey)
        ez20d = np.dot(A02d, self.ez)

        # Derivative of connection array
        r120d = self.body2.v0S0 - self.body1.v0S0

        # Global angular velocities
        om010 = np.dot(A01, self.body1.om0KK)
        om020 = np.dot(A02, self.body2.om0KK)

        # Jgp*z
        Jgpz = np.zeros(4)
        Jgpz[0] = - np.dot(p10.T, np.dot(self.tilde(om010), r120d)) \
            - np.dot(r120.T, np.dot(self.tilde(om010), p10d)) \
            - 2 * np.dot(r120d.T, p10d)
        Jgpz[1] = - np.dot(p20.T, np.dot(self.tilde(om010), r120d)) \
            - np.dot(r120.T, np.dot(self.tilde(om010), p20d)) \
            - 2 * np.dot(r120d.T, p20d)
        # Jgpz[1] = - np.dot(ex10.T, np.dot(self.tilde(om020), ey20d)) \
        #     - np.dot(ey20.T, np.dot(self.tilde(om010), ex10d)) \
        #     - 2 * np.dot(ey20d.T, ex10d)
        Jgpz[2] = - np.dot(ey10.T, np.dot(self.tilde(om020), ez20d)) \
            - np.dot(ez20.T, np.dot(self.tilde(om010), ey10d)) \
            - 2 * np.dot(ez20d.T, ey10d)
        Jgpz[3] = - np.dot(ez10.T, np.dot(self.tilde(om020), ex20d)) \
            - np.dot(ex20.T, np.dot(self.tilde(om010), ez10d)) \
            - 2 * np.dot(ex20d.T, ez10d)

        return Jgpz


class PrismaticHinge_reduced(Constraint):
    dof = 1

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, damp=0, name="PrismaticHinge", save=False):
        Constraint.__init__(self, p1, p2, save)
        self.slide_axis = np.array(axis)
        #self.rotation_axis = np.array(rotation_axis)

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.p11, self.p21 = self.get_perpendicular_axis(self.slide_axis)

        # Initial Connection Array
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        r1P11 = self.p1.rSPK
        r2P22 = self.p2.rSPK
        r0P10 = self.body1.r0S0 + np.dot(A01, r1P11)
        r0P20 = self.body2.r0S0 + np.dot(A02, r2P22)
        self.r0 = r0P20 - r0P10

        self.damp = damp

        self.name = name

        self.Jg1 = np.zeros([1, 6])
        self.Jg2 = np.zeros([1, 6])

    def g(self):
        # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r1P11 = self.p1.rSPK
        r2P22 = self.p2.rSPK
        r0P10 = self.body1.r0S0 + np.dot(A01, r1P11)
        r0P20 = self.body2.r0S0 + np.dot(A02, r2P22)
        rP1P20 = r0P20 - r0P10 - self.r0

        # Two connection constraints
        g1 = np.dot(p10.T, rP1P20)
        g2 = np.dot(p20.T, rP1P20)

        # Two Perpendicular constraints
        g3 = np.dot(ex10.T, ey20)
        g4 = np.dot(ey10.T, ez20)
        g5 = np.dot(ez10.T, ex20)

        return [g2]

    def jacobian(self):
        # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r120 = self.body2.r0S0 - self.body1.r0S0

        # Two connection constraints
        # self.Jg1[0, 0:3] = -p10.T
        # self.Jg1[0, 3:6] = -np.dot(r120.T, np.dot(self.tilde(p10), A01))
        self.Jg1[0, 0:3] = -p20.T
        self.Jg1[0, 3:6] = -np.dot(r120.T, np.dot(self.tilde(p20), A01))

        #self.Jg2[0, 0:3] = p10.T
        self.Jg2[0, 0:3] = p20.T

        # Three perpendicular constraints
        #self.Jg1[2, 3:6] = -np.dot(ey20.T, np.dot(self.tilde(ex10), A01))
        #self.Jg1[2, 3:6] = -np.dot(ez20.T, np.dot(self.tilde(ey10), A01))
        #self.Jg1[1, 3:6] = -np.dot(ex20.T, np.dot(self.tilde(ez10), A01))

        #self.Jg2[2, 3:6] = -np.dot(ex10.T, np.dot(self.tilde(ey20), A02))
        #self.Jg2[2, 3:6] = -np.dot(ey10.T, np.dot(self.tilde(ez20), A02))
        #self.Jg2[1, 3:6] = -np.dot(ez10.T, np.dot(self.tilde(ex20), A02))

        return self.Jg1, self.Jg2

    def djacobian_z(self):
         # Rotation
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Global perpendicular arrays
        p10 = np.dot(A01, self.p11)
        p20 = np.dot(A01, self.p21)

        # Global unit arrays
        ex10 = np.dot(A01, self.ex)
        ey10 = np.dot(A01, self.ey)
        ez10 = np.dot(A01, self.ez)
        ex20 = np.dot(A02, self.ex)
        ey20 = np.dot(A02, self.ey)
        ez20 = np.dot(A02, self.ez)

        # Connection array
        r120 = self.body2.r0S0 - self.body1.r0S0

        # Derivative of rotation matrix
        A01d = self.body1.A0Kd
        A02d = self.body2.A0Kd

        # Derivative of global perpendicular arrays
        p10d = np.dot(A01d, self.p11)
        p20d = np.dot(A01d, self.p21)

        # Derivative of global unit arrays
        ex10d = np.dot(A01d, self.ex)
        ey10d = np.dot(A01d, self.ey)
        ez10d = np.dot(A01d, self.ez)
        ex20d = np.dot(A02d, self.ex)
        ey20d = np.dot(A02d, self.ey)
        ez20d = np.dot(A02d, self.ez)

        # Derivative of connection array
        r120d = self.body2.v0S0 - self.body1.v0S0

        # Global angular velocities
        om010 = np.dot(A01, self.body1.om0KK)
        om020 = np.dot(A02, self.body2.om0KK)

        # Jgp*z
        Jgpz = np.zeros(1)
        # Jgpz[0] = - np.dot(p10.T, np.dot(self.tilde(om010), r120d)) \
        #     - np.dot(r120.T, np.dot(self.tilde(om010), p10d)) \
        #     - 2 * np.dot(r120d.T, p10d)
        Jgpz[0] = - np.dot(p20.T, np.dot(self.tilde(om010), r120d)) \
            - np.dot(r120.T, np.dot(self.tilde(om010), p20d)) \
            - 2 * np.dot(r120d.T, p20d)
        # Jgpz[1] = - np.dot(ex10.T, np.dot(self.tilde(om020), ey20d)) \
        #     - np.dot(ey20.T, np.dot(self.tilde(om010), ex10d)) \
        #     - 2 * np.dot(ey20d.T, ex10d)
        # Jgpz[2] = - np.dot(ey10.T, np.dot(self.tilde(om020), ez20d)) \
        #     - np.dot(ez20.T, np.dot(self.tilde(om010), ey10d)) \
        #     - 2 * np.dot(ez20d.T, ey10d)
        # Jgpz[1] = - np.dot(ez10.T, np.dot(self.tilde(om020), ex20d)) \
        #     - np.dot(ex20.T, np.dot(self.tilde(om010), ez10d)) \
        #     - 2 * np.dot(ex20d.T, ez10d)

        return Jgpz


class PlanarJoint(Constraint):
    dof = 3

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, axis_body: bodies.RigidBody,
                 rotational_damping=0, name="PlanarJoint", save=False):
        Constraint.__init__(self, p1, p2, save)
        self.rotation_axis = np.array(axis)

        self.axis_body = axis_body

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.m2, self.n2 = self.get_perpendicular_axis(self.rotation_axis)

        self.damp = rotational_damping

        self.name = name

    def g(self):
        # Axis for rotational constraints
        s = np.dot(self.body1.A0K, self.ey)
        a = np.dot(self.body2.A0K, self.ex)
        b = np.dot(self.body2.A0K, self.ez)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # Constraint equations
        gy1 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        gy2 = np.dot(m2.T, u2)
        gy3 = np.dot(n2.T, u2)
        return np.hstack((gy1, gy2, gy3))

    def jacobian(self):
        E = np.array([0, 0, 1])
        Z1 = np.zeros([1, 3])

        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        pos1 = np.dot(A01, bodies.tilde(r1B1).T)[2]
        pos2 = -np.dot(A02, bodies.tilde(r2B2).T)[2]

        Jg1 = np.block([[E, pos1],
                        [Z1, -np.dot(self.tilde(m2).T, u2)],
                        [Z1, -np.dot(self.tilde(n2).T, u2)]])

        Jg2 = np.block([[-E, pos2],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(m2).T, u2))],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(n2).T, u2))]])

        return Jg1, Jg2

    def djacobian_z(self):
        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        u2 = self.rotation_axis
        m2 = self.m2
        n2 = self.n2

        om1 = self.body1.om0KK
        om2 = self.body2.om0KK

        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        A01d = self.body1.derivation_rotation_matrix
        A02d = self.body2.derivation_rotation_matrix
        A12dT = np.dot(A01d.transpose(), A02) + np.dot(A01.transpose(), A02d)

        pos = -(np.dot(A01d, np.dot(self.tilde(r1B1).T, om1)) +
                np.dot(A02d, np.dot(self.tilde(r2B2).T, om2)))[2]

        Jgpz = np.block([pos,
                         np.dot(np.dot(A12dT, np.dot(self.tilde(m2).T, u2)), om2),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(n2).T, u2)), om2)])

        return Jgpz


class PlanarJointOne(Constraint):
    dof = 4

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis, axis_body: bodies.RigidBody,
                 rotational_damping=0, name="Hinge", save=False):
        Constraint.__init__(self, p1, p2, save)
        self.rotation_axis = np.array(axis)

        self.axis_body = axis_body

        self.ex = np.array([1, 0, 0])
        self.ey = np.array([0, 1, 0])
        self.ez = np.array([0, 0, 1])

        self.m2, self.n2 = self.get_perpendicular_axis(self.rotation_axis)

        self.damp = rotational_damping

        self.name = name

    def g(self):
        # Axis for rotational constraints
        s = np.dot(self.body1.A0K, self.ey)
        a = np.dot(self.body2.A0K, self.ex)
        b = np.dot(self.body2.A0K, self.ez)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # Constraint equations
        gy1 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK) - \
            (self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK))
        gy2 = np.dot(m2.T, u2)
        gy3 = np.dot(n2.T, u2)
        return np.hstack((gy1, gy2, gy3))

    def jacobian(self):
        E = np.array([[0, 1, 0], [0, 0, 1]])
        Z1 = np.zeros([1, 3])

        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)

        u2 = self.rotation_axis

        m2 = self.m2
        n2 = self.n2

        # first derivation of angular velocity part
        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        pos1 = np.dot(A01, bodies.tilde(r1B1).T)[1:, :]
        pos2 = -np.dot(A02, bodies.tilde(r2B2).T)[1:, :]

        Jg1 = np.block([[A02[:, 1:].T, pos1],
                        [Z1, -np.dot(self.tilde(m2).T, u2)],
                        [Z1, -np.dot(self.tilde(n2).T, u2)]])

        Jg2 = np.block([[-A02[:, 1:].T, pos2],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(m2).T, u2))],
                        [Z1, np.dot(A12.T, np.dot(self.tilde(n2).T, u2))]])

        return Jg1, Jg2

    def djacobian_z(self):
        # rotation axis
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        u2 = self.rotation_axis
        m2 = self.m2
        n2 = self.n2

        om1 = self.body1.om0KK
        om2 = self.body2.om0KK

        r1B1 = self.p1.rSPK
        r2B2 = self.p2.rSPK

        A01d = self.body1.derivation_rotation_matrix
        A02d = self.body2.derivation_rotation_matrix
        A12dT = np.dot(A01d.transpose(), A02) + \
            np.dot(A01.transpose(), A02d)

        pos = -(np.dot(A01d, np.dot(self.tilde(r1B1).T, om1)) +
                np.dot(A02d, np.dot(self.tilde(r2B2).T, om2)))[1:]

        Jgpz = np.block([pos,
                         np.dot(np.dot(A12dT, np.dot(
                             self.tilde(m2).T, u2)), om2),
                         np.dot(np.dot(A12dT, np.dot(self.tilde(n2).T, u2)), om2)])

        return Jgpz


class Orthognal(Constraint):
    dof = 1

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, orthognal_vector1: np.array, orthognal_vector2: np.array):
        Constraint.__init__(self, p1, p2)
        self.s = np.array(orthognal_vector1)
        self.a = np.array(orthognal_vector2)

    def g(self):
        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        gy = np.dot(self.s.T, np.dot(A12, self.a))
        return gy

    def jacobian(self):
        Jg1 = np.zeros([1, 6])
        Jg2 = np.zeros([1, 6])
        Z1 = np.zeros([1, 3])

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        s1 = self.s
        a = self.a

        Jg1[:, 0:3] = Z1
        Jg1[:, 3:6] = -np.dot(s1.T, self.tilde(a).T)

        Jg2[:, 0:3] = Z1
        Jg2[:, 3:6] = np.dot(s1.T, np.dot(A12, self.tilde(a).T))

        return Jg1, Jg2

    def djacobian_z(self):
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K

        # Angular Velocity
        om011 = self.body1.om0KK
        om022 = self.body2.om0KK

        s1 = self.s
        a = self.a

        # derivative of orthognal vectors in inertial system
        s0d = np.dot(A01, np.dot(self.tilde(self.s).T, om011))
        a0d = np.dot(A02, np.dot(self.tilde(self.a).T, om022))

        # derivative of rotation matrix
        A01d = self.p1.body.A0Kd
        A02d = self.p2.body.A0Kd
        A12d = np.dot(A01d.T, A02d)

        return np.dot(s1.T, np.dot(A12d, np.dot(self.tilde(a).T, om022)))


class OrthognalConnect(Constraint):
    dof = 1

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, orthognal_vector1: np.array, save=False):
        Constraint.__init__(self, p1, p2, save)
        self.s = np.array(orthognal_vector1)

    def g(self):
        # Connection vectors
        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0
        r2P22 = self.p2.rSPK

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        d1 = np.dot(A01.T, -r020 + r010) - np.dot(A12, r2P22)

        gy = np.dot(self.s.T, np.dot(A01, d1))
        return gy

    def jacobian(self):
        Jg1 = np.zeros([1, 6])
        Jg2 = np.zeros([1, 6])
        Z1 = np.zeros([1, 3])

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        # Vectors
        s1 = self.s
        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0
        r2P22 = self.p2.rSPK

        Jg1[:, 0:3] = -np.dot(s1.T, A01.T)
        Jg1[:, 3:6] = -np.dot(s1.T, np.dot(A01.T, self.tilde(r020).T)
                              + self.tilde(r2P22).T
                              - np.dot(A01.T, self.tilde(r010).T))

        Jg2[:, 0:3] = np.dot(s1.T, A01.T)
        Jg2[:, 3:6] = np.dot(s1.T, np.dot(A12, self.tilde(r2P22).T))

        return Jg1, Jg2

    def djacobian_z(self):
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0

        # Velocity
        v010 = self.p1.body.v0S0
        v020 = self.p2.body.v0S0

        # Angular Velocity
        om011 = self.body1.om0KK
        om022 = self.body2.om0KK
        om122 = om022 - np.dot(A12.T, om011)

        s1 = self.s
        r2P22 = self.p2.rSPK

        # derivative of rotation matrix
        A01dT = self.p1.body.A0Kd.T
        A01d = self.p1.body.A0Kd
        A02d = self.p2.body.A0Kd
        A12d = np.dot(A01d.T, A02d)

        return np.dot(s1.T, np.dot(A01dT, cross(om011, r020))
                      + np.dot(A01.T, cross(om011, v020))
                      + np.dot(A01dT, v020)
                      - np.dot(A01dT, cross(om011, r010))
                      - np.dot(A01.T, cross(om011, v010))
                      + np.dot(A12d, cross(om122, r2P22))
                      - np.dot(A01dT, v010))


class ReducedOrthognalConnect(Constraint):
    dof = 1

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, orthognal_vector1: np.array, save=False):
        Constraint.__init__(self, p1, p2, save)
        self.s = np.array(orthognal_vector1)

    def g(self):
        # Connection vectors
        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0
        r2P22 = self.p2.rSPK

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        d1 = np.dot(A01.T, -r020 + r010) - np.dot(A12, r2P22)

        gy = np.dot(self.s.T, np.dot(A01, d1))
        return gy

    def jacobian(self):
        Jg1 = np.zeros([1, 6])
        Jg2 = np.zeros([1, 6])
        Z1 = np.zeros([1, 3])

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        # Vectors
        s1 = self.s
        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0
        r2P22 = self.p2.rSPK

        Jg1[:, 0:3] = -np.dot(s1.T, A01.T)
        Jg1[:, 3:6] = -np.dot(s1.T, np.dot(A01.T, self.tilde(r020).T)
                              + self.tilde(r2P22).T
                              - np.dot(A01.T, self.tilde(r010).T))

        return Jg1, Jg2

    def djacobian_z(self):
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0

        # Velocity
        v010 = self.p1.body.v0S0
        v020 = self.p2.body.v0S0

        # Angular Velocity
        om011 = self.body1.om0KK
        om022 = self.body2.om0KK
        om122 = om022 - np.dot(A12.T, om011)

        s1 = self.s
        r2P22 = self.p2.rSPK

        # derivative of rotation matrix
        A01dT = self.p1.body.A0Kd.T
        A01d = self.p1.body.A0Kd
        A02d = self.p2.body.A0Kd
        A12d = np.dot(A01d.T, A02d)

        return np.dot(s1.T, - np.dot(A01dT, cross(om011, r010))
                      - np.dot(A01.T, cross(om011, v010))
                      - np.dot(A01dT, v010))


class OrthognalConnect2(Constraint):
    dof = 1

    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, orthognal_vector1: np.array, save=False):
        Constraint.__init__(self, p1, p2, save)
        self.s = np.array(orthognal_vector1)

    def g(self):
        # Connection vectors
        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0
        r2P22 = self.p2.rSPK

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        d0 = r010 + np.dot(A02, r2P22) + r020
        s0 = np.dot(A01, self.s)

        gy = np.dot(s0.T, d0)
        return gy

    def jacobian(self):
        Jg1 = np.zeros([1, 6])
        Jg2 = np.zeros([1, 6])
        Z1 = np.zeros([1, 3])
        E1 = np.ones([1, 3])

        # rotation matrix
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        # Vectors
        s1 = self.s
        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0
        r2P22 = self.p2.rSPK

        Jg1[:, 0:3] = np.dot(A01, s1)
        Jg1[:, 3:6] = np.dot(np.dot(A12, self.tilde(s1).T),
                             (r020 + np.dot(A02, r2P22) - r010))

        Jg2[:, 0:3] = -np.dot(A01, s1)
        Jg2[:, 3:6] = np.dot(np.dot(A01, s1),
                             np.dot(A02, self.tilde(r2P22).T))

        return Jg1, Jg2

    def djacobian_z(self):
        A01 = self.p1.body.A0K
        A02 = self.p2.body.A0K
        A12 = np.dot(A01.T, A02)

        r010 = self.p1.body.r0S0
        r020 = self.p2.body.r0S0

        # Velocity
        v010 = self.p1.body.v0S0
        v020 = self.p2.body.v0S0

        # Angular Velocity
        om011 = self.body1.om0KK
        om022 = self.body2.om0KK
        om122 = om022 - np.dot(A12.T, om011)

        s1 = self.s
        r2P22 = self.p2.rSPK

        # derivative of rotation matrix
        A01dT = self.p1.body.A0Kd.T
        A01d = self.p1.body.A0Kd
        A02d = self.p2.body.A0Kd
        A12d = np.dot(A01d.T, A02d)

        s0 = np.dot(A01, s1)
        d0 = r020 + np.dot(A02, r2P22) - r010

        s0d = np.dot(A01, cross(om011, s1))
        d0d = v020 + np.dot(A02, cross(om022, r2P22)) + v010

        s0dd_Jgpz = np.dot(A01, cross(om011, cross(om011, s1)))
        d0dd_Jgpz = np.dot(A02, cross(om022, cross(om022, r2P22)))

        gp = np.dot(s0dd_Jgpz, d0) + 2 * np.dot(s0d,
                                                d0dd_Jgpz) + np.dot(s0, d0dd_Jgpz)
        return gp
