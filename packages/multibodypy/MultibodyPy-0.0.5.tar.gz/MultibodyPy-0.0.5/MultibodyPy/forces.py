from typing import Iterable
import numpy as np
from MultibodyPy import bodies
import multiprocessing


def cross(a, b):
    c = [a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0]]

    return np.array(c)


def norm(a):
    return np.sqrt(a[0]**2 + a[1]**2 + a[2]**2)


class Force:
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, save=False, name='Force'):
        self.p1 = p1
        self.p2 = p2
        self.body1 = p1.body
        self.body2 = p2.body

        self.save = save
        if self.save:
            self.force_saver = ForceSaver()

        self.F1 = 0
        self.F2 = 0
        self.M1 = 0
        self.M2 = 0

        self.name = name

    def get_force(self):
        pass


class Bushing(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker,
                 K: np.array, D: np.array, Kr: np.array, Dr: np.array,
                 save=True, name='Bushing'):
        Force.__init__(self, p1, p2, save, name)
        self.K = K
        self.D = D
        self.Kr = Kr
        self.Dr = Dr

        self.u0 = self.u()
        self.phi0 = self.kardan_diff

    def get_force(self):
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        # location of connection points
        rSP10 = np.dot(A01, self.p1.rSPK)
        rSP20 = np.dot(A02, self.p2.rSPK)
        r0P10 = self.body1.r0S0 + rSP10
        r0P20 = self.body2.r0S0 + rSP20

        # velocitiy of connection points
        v010 = self.body1.v0S0
        v020 = self.body2.v0S0
        om011 = self.body1.om0KK
        om022 = self.body2.om0KK
        v01P0 = v010 + np.cross(np.dot(A01, om011), np.dot(A01, self.p1.rSPK))
        v02P0 = v020 + np.cross(np.dot(A02, om022), np.dot(A02, self.p2.rSPK))

        # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
        # in Kardan-Angles
        kardan_12 = self.kardan_diff

        # Forces (Stiffness and Damping)
        dx = (r0P10 - r0P20) - self.u0
        dv = v01P0 - v02P0
        dom = np.dot(self.body1.A0K, self.body1.om0KK) - \
            np.dot(self.body2.A0K, self.body2.om0KK)
        self.F1 = -np.dot(self.K, dx) - np.dot(self.D, dv)
        self.F2 = -self.F1

        # Moments (Stiffness, Damping and spin angular momentum)
        self.M1 = np.cross(rSP10, self.F1) - np.dot(self.Dr,
                                                    dom) + np.dot(self.Kr, kardan_12 - self.phi0)
        self.M2 = np.cross(rSP20, self.F2) + np.dot(self.Dr,
                                                    dom) - np.dot(self.Kr, kardan_12 - self.phi0)

        return self.F1, self.M1, self.F2, self.M2

    def u(self):
        r0P10 = self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK)
        r0P20 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK)
        u = r0P10 - r0P20
        return u

    @property
    def pE0(self):
        r0P10 = self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK)
        r0P20 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK)
        u = r0P10 - r0P20
        return u

    @property
    def kardan_diff(self):
        A01 = self.body1.A0K
        A02 = self.body2.A0K
        A12 = np.dot(A01.T, A02)
        ga_12 = -A12[0, 1]
        be_12 = A12[0, 2]
        al_12 = -A12[1, 2]
        return np.array([al_12, be_12, ga_12])


class Bushing_mp(Bushing):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker,
                 subgroup_1, subgroup_2, q1, q2,
                 K: np.array, D: np.array, Kr: np.array, Dr: np.array,
                 save=True, name='Bushing'):
        super().__init__(p1, p2, K, D, Kr, Dr, save, name)

        self.subgroup_1 = subgroup_1
        self.subgroup_2 = subgroup_2

        A01, _, _ = bodies.RigidBody.rotation_matrix(q1[3:7])
        A02, _, _ = bodies.RigidBody.rotation_matrix(q2[3:7])
        self.phi0 = self.kardan_diff(A01, A02)
        self.F1, self.M1, self.F2, self.M2 = self.get_force(q1, q2)

    def get_force(self, q1, q2):
        # Location
        r010 = q1[0:3]
        r020 = q2[0:3]

        # Rotation Matrix
        A01, _, _ = bodies.RigidBody.rotation_matrix(q1[3:7])
        A02, _, _ = bodies.RigidBody.rotation_matrix(q2[3:7])

        # Velocity
        v010 = q1[7:10]
        v020 = q2[7:10]
        om011 = q1[10:13]
        om022 = q2[10:13]

        # location of connection points
        rSP10 = np.dot(A01, self.p1.rSPK)
        rSP20 = np.dot(A02, self.p2.rSPK)
        r0P10 = r010 + rSP10
        r0P20 = r020 + rSP20

        # velocitiy of connection points
        v01P0 = v010 + np.cross(np.dot(A01, om011), np.dot(A01, self.p1.rSPK))
        v02P0 = v020 + np.cross(np.dot(A02, om022), np.dot(A02, self.p2.rSPK))

        # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
        # in Kardan-Angles
        kardan_12 = self.kardan_diff(A01, A02)

        # Forces (Stiffness and Damping)
        dx = (r0P10 - r0P20) - self.u0
        dv = v01P0 - v02P0
        dom = np.dot(A01, om011) - np.dot(A02, om022)
        F1 = -np.dot(self.K, dx) - np.dot(self.D, dv)
        F2 = -F1

        # Moments (Stiffness, Damping)
        M1 = np.cross(rSP10, F1) - np.dot(self.Dr,
                                          dom) + np.dot(self.Kr, kardan_12 - self.phi0)
        M2 = np.cross(rSP20, F2) + np.dot(self.Dr,
                                          dom) - np.dot(self.Kr, kardan_12 - self.phi0)
        self.F1, self.M1, self.F2, self.M2 = F1, M1, F2, M2
        return F1, M1, F2, M2

    def kardan_diff(self, A01, A02):
        A12 = np.dot(A01.T, A02)
        ga_12 = -A12[0, 1]
        be_12 = A12[0, 2]
        al_12 = -A12[1, 2]
        return np.array([al_12, be_12, ga_12])


class BushingLocal_mp(Bushing_mp):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker,
                 subgroup_1, subgroup_2, q1, q2,
                 K: np.array, D: np.array, Kr: np.array, Dr: np.array,
                 save=True, name='Bushing'):
        self.q1 = q1
        self.q2 = q2
        super().__init__(p1, p2, subgroup_1, subgroup_2, q1, q2, K, D, Kr, Dr, save, name)
        self.F1, self.M1, self.F2, self.M2 = self.get_force(q1, q2)

    def get_force(self, q1, q2):
        # Location
        r010 = q1[0:3]
        r020 = q2[0:3]

        # Rotation Matrix
        A01, _, _ = bodies.RigidBody.rotation_matrix(q1[3:7])
        A02, _, _ = bodies.RigidBody.rotation_matrix(q2[3:7])

        # Velocity
        v010 = q1[7:10]
        v020 = q2[7:10]
        om011 = q1[10:13]
        om022 = q2[10:13]

        # location of connection points
        rSP10 = np.dot(A01, self.p1.rSPK)
        rSP20 = np.dot(A02, self.p2.rSPK)
        r0P10 = r010 + rSP10
        r0P20 = r020 + rSP20
        r120 = r0P10 - r0P20
        r121 = np.dot(A01.T, r120)

        # velocitiy of connection points
        v01P0 = v010 + np.cross(np.dot(A01, om011), np.dot(A01, self.p1.rSPK))
        v02P0 = v020 + np.cross(np.dot(A02, om022), np.dot(A02, self.p2.rSPK))
        v120 = v01P0 - v02P0
        v121 = np.dot(A01.T, v120)

        # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
        # in Kardan-Angles
        kardan_12 = self.kardan_diff(A01, A02)

        # Forces (Stiffness and Damping)
        dx = r121 - self.u0
        dv = v121
        dom = np.dot(A01, om011) - np.dot(A02, om022)
        F11 = -np.dot(self.K, dx) - np.dot(self.D, dv)
        F22 = -F11

        F1 = np.dot(A01, F11)
        F2 = np.dot(A01, F22)

        # Moments (Stiffness, Damping)
        M1 = np.cross(rSP10, F1) - np.dot(self.Dr,
                                          dom) + np.dot(self.Kr, kardan_12 - self.phi0)
        M2 = np.cross(rSP20, F2) + np.dot(self.Dr,
                                          dom) - np.dot(self.Kr, kardan_12 - self.phi0)
        self.F1, self.M1, self.F2, self.M2 = F1, M1, F2, M2
        return F1, M1, F2, M2

    def u(self):
        A01, _, _ = bodies.RigidBody.rotation_matrix(self.q1[3:7])
        A02, _, _ = bodies.RigidBody.rotation_matrix(self.q2[3:7])
        r0P10 = self.q1[0:3] + np.dot(A01, self.p1.rSPK)
        r0P20 = self.q2[0:3] + np.dot(A02, self.p2.rSPK)
        u = r0P10 - r0P20
        u1 = np.dot(A01.T, u)
        return u1


class BushingLocalGap_mp(Bushing_mp):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker,
                 subgroup_1, subgroup_2, q1, q2, gap, gap_dir,
                 K: np.array, D: np.array, Kr: np.array, Dr: np.array,
                 save=True, name='Bushing'):
        self.q1 = q1
        self.q2 = q2
        self.gap = gap
        self.gap_dir = np.array(gap_dir)
        super().__init__(p1, p2, subgroup_1, subgroup_2, q1, q2, K, D, Kr, Dr, save, name)
        self.F1, self.M1, self.F2, self.M2 = self.get_force(q1, q2)

    def get_force(self, q1, q2):
        # Location
        r010 = q1[0:3]
        r020 = q2[0:3]

        # Rotation Matrix
        A01, _, _ = bodies.RigidBody.rotation_matrix(q1[3:7])
        A02, _, _ = bodies.RigidBody.rotation_matrix(q2[3:7])

        # Velocity
        v010 = q1[7:10]
        v020 = q2[7:10]
        om011 = q1[10:13]
        om022 = q2[10:13]

        # location of connection points
        rSP10 = np.dot(A01, self.p1.rSPK)
        rSP20 = np.dot(A02, self.p2.rSPK)
        r0P10 = r010 + rSP10
        r0P20 = r020 + rSP20
        r120 = r0P10 - r0P20
        r121 = np.dot(A01.T, r120)

        # velocitiy of connection points
        v01P0 = v010 + np.cross(np.dot(A01, om011), np.dot(A01, self.p1.rSPK))
        v02P0 = v020 + np.cross(np.dot(A02, om022), np.dot(A02, self.p2.rSPK))
        v120 = v01P0 - v02P0
        v121 = np.dot(A01.T, v120)

        # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
        # in Kardan-Angles
        kardan_12 = self.kardan_diff(A01, A02)

        # Forces (Stiffness and Damping)
        dx = r121 - self.u0
        dv = v121
        dom = np.dot(A01, om011) - np.dot(A02, om022)
        if np.abs(np.dot(self.gap_dir, dx)) > self.gap:
            d = np.dot(self.gap_dir, dx) - \
                np.sign(np.dot(self.gap_dir, dx)) * self.gap
            F11 = -np.dot(self.K, d * self.gap_dir) - np.dot(self.D, dv)
        else:
            F11 = np.zeros(3)
        F22 = -F11

        F1 = np.dot(A01, F11)
        F2 = np.dot(A01, F22)

        # Moments (Stiffness, Damping)
        M1 = np.cross(rSP10, F1) - np.dot(self.Dr,
                                          dom) + np.dot(self.Kr, kardan_12 - self.phi0)
        M2 = np.cross(rSP20, F2) + np.dot(self.Dr,
                                          dom) - np.dot(self.Kr, kardan_12 - self.phi0)
        self.F1, self.M1, self.F2, self.M2 = F1, M1, F2, M2
        return F1, M1, F2, M2

    def u(self):
        A01, _, _ = bodies.RigidBody.rotation_matrix(self.q1[3:7])
        A02, _, _ = bodies.RigidBody.rotation_matrix(self.q2[3:7])
        r0P10 = self.q1[0:3] + np.dot(A01, self.p1.rSPK)
        r0P20 = self.q2[0:3] + np.dot(A02, self.p2.rSPK)
        u = r0P10 - r0P20
        u1 = np.dot(A01.T, u)
        return u1


class BushingLocal(Bushing):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker,
                 K: np.array, D: np.array, Kr: np.array, Dr: np.array,
                 save=True, name='BushingLocal'):
        super().__init__(p1, p2, K, D, Kr, Dr, save, name)
        self.u0 = self.u()

    def get_force(self):
        A01 = self.body1.A0K
        r010 = self.body1.r0S0
        A02 = self.body2.A0K
        r020 = self.body2.r0S0

        # location of connection points
        r120 = r010 + np.dot(A01, self.p1.rSPK) - r020 - \
            np.dot(A02, self.p2.rSPK)
        r121 = np.dot(A01.T, r120)

        # velocitiy of connection points
        v01P0 = self.body1.v0S0 + np.cross(self.body1.om0KK, self.p1.rSPK)
        v02P0 = self.body2.v0S0 + np.cross(self.body2.om0KK, self.p2.rSPK)
        v120 = v01P0 - v02P0
        v121 = np.dot(A01.T, v120)

        # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
        # in Kardan-Angles
        kardan_12 = self.kardan_diff

        # Forces (Stiffness and Damping)
        dx = r121 - self.u0
        dv = v121
        dom = np.dot(self.body1.A0K, self.body1.om0KK) - \
            np.dot(self.body2.A0K, self.body2.om0KK)
        F11 = -np.dot(self.K, dx) - np.dot(self.D, dv)
        F22 = -F11

        F10 = np.dot(A01, F11)
        F20 = np.dot(A01, F22)

        self.F1 = F10
        self.F2 = F20

        # Moments (Stiffness, Damping and spin angular momentum)
        rSP10 = np.dot(self.body1.A0K, self.p1.rSPK)
        rSP20 = np.dot(self.body2.A0K, self.p2.rSPK)
        self.M1 = np.cross(rSP10, self.F1) - np.dot(self.Dr,
                                                    dom) + np.dot(self.Kr, kardan_12 - self.phi0)
        self.M2 = np.cross(rSP20, self.F2) + np.dot(self.Dr,
                                                    dom) - np.dot(self.Kr, kardan_12 - self.phi0)
        # self.F1 = F11
        # self.F2 = F22
        return F10, self.M1, F20, self.M2

    def u(self):
        r0P10 = self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK)
        r0P20 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK)
        u = r0P10 - r0P20
        u1 = np.dot(self.body1.A0K.T, u)
        return u1


class BushingLocalGap(Bushing):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker,
                 K: np.array, D: np.array, Kr: np.array, Dr: np.array,
                 gap=0, gap_dir=[1, 0, 0], save=True, name='BushingLocalGap'):
        super().__init__(p1, p2, K, D, Kr, Dr, save, name)
        self.u0 = self.u()
        self.gap = gap
        self.gap_dir = np.array(gap_dir)

    def get_force(self):
        A01 = self.body1.A0K
        r010 = self.body1.r0S0
        A02 = self.body2.A0K
        r020 = self.body2.r0S0

        # location of connection points
        r120 = r010 + np.dot(A01, self.p1.rSPK) - r020 - \
            np.dot(A02, self.p2.rSPK)
        r121 = np.dot(A01.T, r120)

        # velocitiy of connection points
        v01P0 = self.body1.v0S0 + np.cross(self.body1.om0KK, self.p1.rSPK)
        v02P0 = self.body2.v0S0 + np.cross(self.body2.om0KK, self.p2.rSPK)
        v120 = v01P0 - v02P0
        v121 = np.dot(A01.T, v120)

        # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
        # in Kardan-Angles
        kardan_12 = self.kardan_diff

        # Forces (Stiffness and Damping)
        dx = r121 - self.u0
        dv = v121
        dom = np.dot(self.body1.A0K, self.body1.om0KK) - \
            np.dot(self.body2.A0K, self.body2.om0KK)

        if np.abs(np.dot(self.gap_dir, dx)) > self.gap:
            d = np.dot(self.gap_dir, dx) - \
                np.sign(np.dot(self.gap_dir, dx)) * self.gap
            F11 = -np.dot(self.K, d * self.gap_dir) - np.dot(self.D, dv)
        else:
            F11 = np.zeros(3)
        F22 = -F11

        F10 = np.dot(A01, F11)
        F20 = np.dot(A01, F22)

        self.F1 = F10
        self.F2 = F20

        # Moments (Stiffness, Damping and spin angular momentum)
        rSP10 = np.dot(self.body1.A0K, self.p1.rSPK)
        rSP20 = np.dot(self.body2.A0K, self.p2.rSPK)
        self.M1 = np.cross(rSP10, self.F1) - np.dot(self.Dr,
                                                    dom) + np.dot(self.Kr, kardan_12 - self.phi0)
        self.M2 = np.cross(rSP20, self.F2) + np.dot(self.Dr,
                                                    dom) - np.dot(self.Kr, kardan_12 - self.phi0)
        # self.F1 = F11
        # self.F2 = F22
        return F10, self.M1, F20, self.M2

    def u(self):
        r0P10 = self.body1.r0S0 + np.dot(self.body1.A0K, self.p1.rSPK)
        r0P20 = self.body2.r0S0 + np.dot(self.body2.A0K, self.p2.rSPK)
        u = r0P10 - r0P20
        u1 = np.dot(self.body1.A0K.T, u)
        return u1


class PointForce(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, F, move_with_body=False, save=False, name='PointForce'):
        Force.__init__(self, p1, p2, save, name)
        self.F = np.array(F)
        self.move_with_body = move_with_body

    def get_force(self):
        # Force Point on 1
        rSP10 = np.dot(self.body1.A0K, self.p1.rSPK)

        # Forces
        if self.move_with_body:
            self.F1 = np.dot(self.body1.A0K, self.F)
        else:
            self.F1 = self.F
        self.F2 = -self.F1

        # Moments
        self.M1 = np.cross(rSP10, self.F1)
        self.M2 = -self.M1

        return self.F1, self.M1, self.F2, self.M2


class PointMoment(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, M, save=False, name='PointMoment'):
        Force.__init__(self, p1, p2, save, name)
        self.M = np.array(M)

    def get_force(self):
        # Forces
        self.F1 = np.zeros(3)
        self.F2 = self.F1

        # Moments
        self.M1 = self.M
        self.M2 = -self.M

        return self.F1, self.M1, self.F2, self.M2


class PointForceLoc(PointForce):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, F: np.array, left_boundary=0, right_boundary=np.inf,
                 move_with_body=False, save=False, name='PointForceLoc'):
        PointForce.__init__(self, p1, p2, F, move_with_body, save, name)
        self.bs = left_boundary
        self.be = right_boundary

    def get_force(self):
        # Force Point on 1
        rSP10 = np.dot(self.body1.A0K, self.p1.rSPK)
        rSP20 = np.dot(self.body2.A0K, self.p2.rSPK)

        # Forces
        if not any(self.p1.rSPK > self.be) and not any(self.p1.rSPK < self.bs):
            if self.move_with_body:
                self.F1 = np.dot(self.body1.A0K, self.F)
            else:
                self.F1 = self.F
        else:
            self.F1 = np.zeros(3)
        self.F2 = -self.F1

        # Moments
        self.M1 = np.cross(rSP10, self.F1)
        self.M2 = np.cross(rSP20, self.F2)

        return self.F1, self.M1, self.F2, self.M2


class DampingForce(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, damping: np.array, save=False, name='DampingForce'):
        super().__init__(p1, p2, save, name)
        self.damping = np.diag(damping)

    def get_force(self):
        v1 = self.p1.body.v0S0
        v2 = self.p2.body.v0S0
        A02 = self.p2.body.A0K

        dv = v2 - v1
        dv2 = np.dot(A02, dv)

        F = np.dot(self.damping, dv2)

        return F, np.zeros(3), -F, np.zeros(3)


class ForceSaver:
    def __init__(self):
        self.F = None

    def save(self, F: np.array):
        if self.F is None:
            self.F = F
        else:
            self.F = np.vstack((self.F, F))


class Contact(Force):
    def __init__(self, body1: bodies.RigidBody, body2: bodies.RigidBody, p1: bodies.Marker, p2: bodies.Marker, n2: np.array, k, d, fric=None, save=True, name='Contact'):
        Force.__init__(self, p1, p2, save, name)
        self.body1 = body1
        self.body2 = body2
        self.n2 = np.array(n2)
        self.k = k
        self.d = d
        self.fric = fric

    def get_force(self):
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Point locations
        r1P0 = np.dot(A01, self.p1.rSPK)
        r2P0 = np.dot(A02, self.p2.rSPK)

        # get current gap and velocity
        dn, vn = self.get_gap_velcotiy_normal
        # compute contact normal force
        if dn < 0:
            Fn = self.get_normal_force(dn, vn)

            if self.fric is not None:
                vt, et = self.get_velocity_tangential
                Ft = -self.fric.get_friction_force(Fn, vt)
            else:
                Ft = 0
                et = 0

            F = Fn * self.n2 + Ft * et

        else:
            F = np.zeros(3)

        # forces and moments acting on bodies
        self.F1 = -np.dot(A02, F)
        self.F2 = np.dot(A02, F)
        self.M1 = np.dot(A01.T, cross(r1P0, self.F1))
        self.M2 = np.dot(A02.T, cross(r2P0, self.F2))
        # self.M1 = np.cross(r1P1, self.F1)
        # self.M2 = np.cross(r2P2, self.F2)

        return self.F1, self.M1, self.F2, self.M2

    def get_normal_force(self, dn, vn):
        return 0

    @property
    def get_velocity_tangential(self):
        # location of bodies
        r010 = self.body1.r0S0
        r020 = self.body2.r0S0

        # velocities of bodies
        v010 = self.body1.v0S0
        v020 = self.body2.v0S0

        # rotation matrices
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # derivation of rotation matrices
        A01d = self.body1.A0Kd
        A02d = self.body2.A0Kd

        # local location of Points
        r1P1 = self.p1.rSPK
        r2P2 = self.p2.rSPK

        # Velocity Vector betwwen Contact Points
        d0d = v010 + np.dot(A01d, r1P1) - v020 - np.dot(A02d, r2P2)

        # Transform to plane coordinate system
        d2d = np.dot(A02.T, d0d)

        # Perpendicular Vector to plane
        v = np.dot(d2d.T, self.n2)

        # Tangential velocity
        vt2 = d2d - v * self.n2
        vt2n = norm(vt2)

        # Tangential direction
        if vt2n != 0:
            et2 = vt2 / vt2n
        else:
            et2 = np.array([0, 0, 0])

        return vt2, et2

    @property
    def get_gap_velcotiy_normal(self):
        # location of bodies
        r010 = self.body1.r0S0
        r020 = self.body2.r0S0

        # velocities of bodies
        v010 = self.body1.v0S0
        v020 = self.body2.v0S0

        # rotation matrices
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # derivation of rotation matrices
        A01d = self.body1.A0Kd
        A02d = self.body2.A0Kd

        # local location of Points
        r1P1 = self.p1.rSPK
        r2P2 = self.p2.rSPK

        # Location Vector between Contact Points
        d0 = r010 + np.dot(A01, r1P1) - r020 - np.dot(A02, r2P2)

        # Velocity Vector betwwen Contact Points
        d0d = v010 + np.dot(A01d, r1P1) - v020 - np.dot(A02d, r2P2)

        # Transform to plane coordinate system
        d2 = np.dot(A02.T, d0)
        d2d = np.dot(A02.T, d0d)

        # Perpendicular Vector to plane
        d = np.dot(d2.T, self.n2)
        v = np.dot(d2d.T, self.n2)

        return d, v


class ContactlessFriction(Contact):
    def __init__(self, p1,
                 p2,
                 n2, mud, vd, Fn, save=True, name='ContactlessFriction'):
        Force.__init__(self, p1, p2, save, name)
        self.n2 = np.array(n2)
        self.mud = mud
        self.vd = vd
        self.Fn = Fn

    def get_force(self):
        q1 = np.concatenate((self.p1.body.y, self.p1.body.z))
        q2 = np.concatenate((self.p2.body.y, self.p2.body.z))

        # Rotation Matrix
        A01, _, L1 = bodies.RigidBody.rotation_matrix(q1[3:7])
        A02, _, L2 = bodies.RigidBody.rotation_matrix(q2[3:7])

        # Point locations
        r1P0 = np.dot(A01, self.p1.rSPK)
        r2P0 = np.dot(A02, self.p2.rSPK)

        # get current gap and velocity
        vt, et = self.get_velocity_tangential(A01, A02, L1, L2, q1, q2)
        Ft = self.get_friction_force(self.Fn, vt)
        F = Ft * et

        # forces and moments acting on bodies
        self.F1 = -np.dot(A02, F)
        self.F2 = np.dot(A02, F)
        self.M1 = np.dot(A01.T, cross(r1P0, self.F1))
        self.M2 = np.dot(A02.T, cross(r2P0, self.F2))
        # self.M1 = np.cross(r1P1, self.F1)
        # self.M2 = np.cross(r2P2, self.F2)

        return self.F1, self.M1, self.F2, self.M2

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # linear Friction force when 0<v<vd
        if vtabs < self.vd:
            Ft = self.mud * vtabs * Fn / self.vd
        else:
            Ft = self.mud * Fn

        return Ft

    def get_velocity_tangential(self, A01, A02, L1, L2, q1, q2):
        # location of bodies
        r010 = q1[0:3]
        r020 = q2[0:3]

        # velocities of bodies
        v010 = q1[7:10]
        v020 = q2[7:10]

        # derivation of rotation matrices
        A01d = self.derivation_rotation_matrix(L1, q1[10:13])
        A02d = self.derivation_rotation_matrix(L2, q2[10:13])

        # local location of Points
        r1P1 = self.p1.rSPK
        r2P2 = self.p2.rSPK

        # Velocity Vector betwwen Contact Points
        d0d = v010 + np.dot(A01d, r1P1) - v020 - np.dot(A02d, r2P2)

        # Transform to plane coordinate system
        d2d = np.dot(A02.T, d0d)

        # Perpendicular Vector to plane
        v = np.dot(d2d.T, self.n2)

        # Tangential velocity
        vt2 = d2d - v * self.n2
        vt2n = norm(vt2)

        # Tangential direction
        if vt2n != 0:
            et2 = vt2 / vt2n
        else:
            et2 = np.array([0, 0, 0])

        return vt2, et2

    @staticmethod
    def derivation_rotation_matrix(L, om0KK):
        pEp = 0.5 * np.dot(L.transpose(), om0KK)
        _, Gp, _ = bodies.RigidBody.rotation_matrix(pEp)
        A0Kd = 2 * np.dot(Gp, L.transpose())
        return A0Kd


class ContactlessFriction_mp(Contact):
    def __init__(self, p1,
                 p2,
                 subgroup_1,
                 subgroup_2,
                 q1, q2,
                 n2, mud, vd, Fn, save=True, name='ContactlessFriction_mp'):
        Force.__init__(self, p1, p2, save, name)
        self.n2 = np.array(n2)
        self.mud = mud
        self.vd = vd
        self.Fn = Fn

        self.subgroup_1 = subgroup_1
        self.subgroup_2 = subgroup_2
        self.F1, self.M1, self.F2, self.M2 = self.get_force(q1, q2)

    def get_force(self, q1, q2):
        # Rotation Matrix
        A01, _, L1 = bodies.RigidBody.rotation_matrix(q1[3:7])
        A02, _, L2 = bodies.RigidBody.rotation_matrix(q2[3:7])

        # Point locations
        r1P0 = np.dot(A01, self.p1.rSPK)
        r2P0 = np.dot(A02, self.p2.rSPK)

        # get current gap and velocity
        vt, et = self.get_velocity_tangential(A01, A02, L1, L2, q1, q2)
        Ft = self.get_friction_force(self.Fn, vt)

        F = Ft * et

        # forces and moments acting on bodies
        self.F1 = -np.dot(A02, F)
        self.F2 = np.dot(A02, F)
        self.M1 = np.dot(A01.T, cross(r1P0, self.F1))
        self.M2 = np.dot(A02.T, cross(r2P0, self.F2))
        # self.M1 = np.cross(r1P1, self.F1)
        # self.M2 = np.cross(r2P2, self.F2)

        return self.F1, self.M1, self.F2, self.M2

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # linear Friction force when 0<v<vd
        if vtabs < self.vd:
            Ft = self.mud * vtabs * Fn / self.vd
        else:
            Ft = self.mud * Fn

        return Ft

    def get_velocity_tangential(self, A01, A02, L1, L2, q1, q2):
        # location of bodies
        r010 = q1[0:3]
        r020 = q2[0:3]

        # velocities of bodies
        v010 = q1[7:10]
        v020 = q2[7:10]

        # derivation of rotation matrices
        A01d = self.derivation_rotation_matrix(L1, q1[10:13])
        A02d = self.derivation_rotation_matrix(L2, q2[10:13])

        # local location of Points
        r1P1 = self.p1.rSPK
        r2P2 = self.p2.rSPK

        # Velocity Vector betwwen Contact Points
        d0d = v010 + np.dot(A01d, r1P1) - v020 - np.dot(A02d, r2P2)

        # Transform to plane coordinate system
        d2d = np.dot(A02.T, d0d)

        # Perpendicular Vector to plane
        v = np.dot(d2d.T, self.n2)

        # Tangential velocity
        vt2 = d2d - v * self.n2
        vt2n = norm(vt2)

        # Tangential direction
        if vt2n != 0:
            et2 = vt2 / vt2n
        else:
            et2 = np.array([0, 0, 0])

        return vt2, et2

    @staticmethod
    def derivation_rotation_matrix(L, om0KK):
        pEp = 0.5 * np.dot(L.transpose(), om0KK)
        _, Gp, _ = bodies.RigidBody.rotation_matrix(pEp)
        A0Kd = 2 * np.dot(Gp, L.transpose())
        return A0Kd


class KelvinVoigtContact(Contact):
    def __init__(self, body1: bodies.RigidBody, body2: bodies.RigidBody, p1: bodies.Marker, p2: bodies.Marker, n2: np.array, k, d, fric=None, save=True, name='KelvinVoigtContact'):
        Contact.__init__(self, body1, body2, p1, p2,
                         n2, k, d, fric, save, name)

    def get_normal_force(self, dn, vn):
        Fk = self.k * dn
        Fd = self.d * vn

        # Damping !< Contact Force to prevent contact sticking
        if np.abs(Fd) > np.abs(Fk):
            Fd = np.sign(Fd) * np.abs(Fk)
        F = Fk + Fd
        return F


class Friction:
    def __init__(self, mud, vd):
        self.mud = mud
        self.vd = vd

    def get_friction_force(self, Fn, vt):
        return 0


class SimpleFriction(Friction):
    def __init__(self, mud, vd):
        Friction.__init__(self, mud, vd)

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # linear Friction force when 0<v<vd
        if vtabs < self.vd:
            Ft = self.mud * vtabs * Fn / self.vd
        else:
            Ft = self.mud * Fn

        return Ft


class BilinearFriction(Friction):
    def __init__(self, mud, vd, mus, vs):
        Friction.__init__(self, mud, vd)
        self.mus = mus
        self.vs = vs

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # linear Friction force when 0<v<vd
        if vtabs < self.vs:
            Ft = self.mus * vtabs * Fn / self.vs
        else:
            md = (self.mud - self.mus) / (self.vd - self.vs)
            td = self.mud - md * self.vd
            Ft = md * vtabs + td

        return Ft


class SigmoidFriction(Friction):
    def __init__(self, mud, vd):
        Friction.__init__(self, mud, vd)

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # sigmoid Friction force
        mu = 2 * self.mud / (1 + np.exp(-6 / self.vd * vtabs)) + self.mud

        Ft = mu * Fn

        return Ft


class HyperbolicTangensFriction(Friction):
    def __init__(self, mud, vd):
        Friction.__init__(self, mud, vd)

    def get_friction_force(self, Fn, vt):
         # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # Hyperbolic Tangens Friction
        mu = self.mud * np.tanh(vtabs / (self.vd / 2.6))

        # Friction Force
        Ft = mu * Fn

        return Ft


class StribeckFriction(Friction):
    def __init__(self, mus, vs, mud, vd):
        Friction.__init__(self, mud, vd)
        self.mus = mus
        self.vs = vs

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # linear Friction force when 0<v<vd
        if 0 <= np.abs(vtabs) <= self.vs:
            mu = self.mus * vtabs / self.vs
        elif self.vs < np.abs(vtabs) <= self.vd:
            m = (self.mud - self.mus) / (self.vd - self.vs)
            t = np.sign(vtabs) * (self.mus * self.vd - self.mud *
                                  self.vs) / (self.vd - self.vs)
            mu = m * vtabs + t
        else:
            mu = np.sign(vtabs) * self.mud

        Ft = mu * Fn

        return Ft


class BilinearStribeckFriction(Friction):
    def __init__(self, mus, vs, mud, vd, m):
        Friction.__init__(self, mud, vd)
        self.mus = mus
        self.vs = vs
        self.m = m

    def get_friction_force(self, Fn, vt):
        # absolute tangential velocity
        vtabs = np.linalg.norm(vt)

        # linear Friction force when 0<v<vd
        if 0 <= np.abs(vtabs) <= self.vs:
            mu = self.mus * vtabs / self.vs
        elif self.vs < np.abs(vtabs) <= self.vd:
            m = (self.mud - self.mus) / (self.vd - self.vs)
            t = np.sign(vtabs) * (self.mus * self.vd - self.mud *
                                  self.vs) / (self.vd - self.vs)
            mu = m * vtabs + t
        else:
            t = np.sign(vtabs) * (self.mud - self.m * self.vd)
            mu = (self.m * vtabs + t)

        Ft = mu * Fn

        return Ft


class ConstantDamper(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, vd, Fd, save=False, name='SimpleHydraulicDamper'):
        Force.__init__(self, p1, p2, save, name)
        self.vd = vd
        self.Fd = Fd

    def get_force(self):
        # velocitiy of connection points
        v01P0 = self.body1.v0S0 + np.cross(self.body1.om0KK, self.p1.rSPK)
        v02P0 = self.body2.v0S0 + np.cross(self.body2.om0KK, self.p2.rSPK)

        # velocitiy between connection points
        v120 = v01P0 - v02P0

        # linear force when 0<v<vd
        F = []
        for i in range(0, 3):
            if np.abs(v120[i]) < self.vd[i]:
                F.append(self.Fd[i] * v120[i] / self.vd[i])
            else:
                F.append(np.sign(v120[i]) * self.Fd[i])

        self.F1 = -np.array(F)
        self.M1 = -np.zeros(3)
        self.F2 = np.array(F)
        self.M2 = np.zeros(3)

        return self.F1, self.M1, self.F2, self.M2


class BilinearDamper(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, v1, Fd1, v2, Fd2, save=False, name='SimpleHydraulicDamper'):
        Force.__init__(self, p1, p2, save, name)
        self.v1 = v1
        self.Fd1 = Fd1

        self.v2 = v2
        self.Fd2 = Fd2

    def get_force(self):
        # velocitiy of connection points
        v01P0 = self.body1.v0S0 + np.cross(self.body1.om0KK, self.p1.rSPK)
        v02P0 = self.body2.v0S0 + np.cross(self.body2.om0KK, self.p2.rSPK)

        # velocitiy between connection points
        v120 = v01P0 - v02P0

        # linear force when 0<v<vd
        F = []
        for i in range(0, 3):
            if np.abs(v120[i]) < self.v1[i]:
                F.append(self.Fd1[i] * v120[i] / self.v1[i])
            else:
                m2 = (self.Fd2[i] - self.Fd1[i]) / (self.v2[i] - self.v1[i])
                t2 = self.Fd2[i] - m2 * self.v2[i]
                F.append(m2 * v120[i] + np.sign(v120[i]) * t2)

        self.F1 = -np.array(F)
        self.M1 = -np.zeros(3)
        self.F2 = np.array(F)
        self.M2 = np.zeros(3)

        return self.F1, self.M1, self.F2, self.M2


class HyperbolicTangensDamper(Force):
    def __init__(self, p1: bodies.Marker, p2: bodies.Marker, axis: Iterable, vd, Fd, save=False, name='HyperbolicDamper'):
        Force.__init__(self, p1, p2, save, name)
        self.vd = vd
        self.Fd = Fd
        self.s1 = np.array(axis)

    def get_force(self):
        # Rotation matrix
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # Locations
        r1P10 = np.dot(A01, self.p1.rSPK)
        r2P20 = np.dot(A02, self.p2.rSPK)

        # Velocity
        om010 = np.dot(A01, self.body1.om0KK)
        om020 = np.dot(A02, self.body2.om0KK)
        vP1P20 = self.body1.v0S0 + \
            np.cross(om010, r1P10) - self.body2.v0S0 + np.cross(om020, r2P20)
        vP1P21 = np.dot(A01.T, vP1P20)
        v_res = np.dot(vP1P21, self.s1)

        # Tangential force
        Ft = self.Fd * np.tanh(v_res / (self.vd / 2.6))

        # Local force
        F1 = Ft * self.s1

        # Global Force
        F0 = np.dot(A01, F1)

        # Resulting Forces
        self.F1 = -F0
        self.F2 = F0
        self.M1 = np.dot(A01.T, cross(r1P10, self.F1))
        self.M2 = np.dot(A02.T, cross(r2P20, self.F2))

        return self.F1, self.M1, self.F2, self.M2

    @property
    def get_velocity_tangential(self):
        # location of bodies
        r010 = self.body1.r0S0
        r020 = self.body2.r0S0

        # velocities of bodies
        v010 = self.body1.v0S0
        v020 = self.body2.v0S0

        # rotation matrices
        A01 = self.body1.A0K
        A02 = self.body2.A0K

        # derivation of rotation matrices
        A01d = self.body1.A0Kd
        A02d = self.body2.A0Kd

        # local location of Points
        r1P1 = self.p1.rSPK
        r2P2 = self.p2.rSPK

        # Velocity Vector betwwen Contact Points
        d0d = v010 + np.dot(A01d, r1P1) - v020 - np.dot(A02d, r2P2)

        # Transform to plane coordinate system
        d2d = np.dot(A02.T, d0d)

        # Tangential velocity
        vt2 = d2d
        vt2n = norm(vt2)

        # Tangential direction
        if vt2n != 0:
            et2 = vt2 / vt2n
        else:
            et2 = np.array([0, 0, 0])

        return vt2, et2
