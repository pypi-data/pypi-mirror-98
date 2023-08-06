import numpy as np
import pandas as pd
from numba import njit, prange
import pickle


# @njit(cache=True)
def move(t):
    return np.array([0.2, 0.0, 0.0]) * np.sin(0.2 * 2 * np.pi * t)


# @njit(cache=True)
def qdot(t, q, bodies, bushings, frictions, joints, prismatics, mass):
    # Position and Velocity
    y = q[0:int(len(bodies) * 7)]
    z = q[int(len(bodies) * 7):]
    qe = np.zeros(len(bodies) * 6)

    # external forces
    qe = qe + external_forces(t, y, z, bodies, bushings, frictions)

    # Graviation
    qe = qe + gravitation_forces(bodies)

    # spin angular momentum
    qe = qe + spin_angular_momentum(y, z, bodies)

    # constraint forces
    con_force, con_z = constraint_force_velocity(
        t, y, z, bodies, joints, prismatics, mass, qe)
    qe = qe + con_force
    z = z + con_z

    # kinematic ode
    yp = kinematic_ode(y, z, bodies)

    # dynamic ode
    zp = np.linalg.solve(mass, qe)

    # state change
    qp = np.concatenate((yp, zp))
    return qp


# @njit(cache=True)
def jacobian(t, q, bodies, bushings, frictions, joints, mass):
    epsilon = 1e-8
    func = qdot
    f0 = func(t, q, bodies, bushings, frictions, joints, mass)
    jac = np.zeros((len(q), len(f0)))
    for i in prange(len(q)):
        dx = np.zeros(len(q))
        dx[i] = epsilon
        f1 = func(t, q + dx, bodies, bushings, frictions, joints, mass)
        jac[i] = (f1 - f0) / (epsilon)
    return jac.transpose()


# @njit(cache=True)
def external_forces(t, y, z, bodies, forces, frictions):
    qe = np.zeros(len(bodies) * 6)
    for i in prange(0, len(forces)):
        force = forces[i]
        posy1 = int(force.body1.pos * 7)
        posz1 = int(force.body1.pos * 6)
        y1 = y[posy1: posy1 + 7]
        z1 = z[posz1: posz1 + 6]
        q1 = np.concatenate((y1, z1))
        if force.body2.name == 'Ground':
            q2 = force.body2.q0
        else:
            posy2 = int(force.body2.pos * 7)
            posz2 = int(force.body2.pos * 6)
            y2 = y[posy2: posy2 + 7]
            z2 = z[posz2: posz2 + 6]
            q2 = np.concatenate((y2, z2))

        if force.name == 'Move':
            rSP1 = force.rSP1
            rSP2 = move(t)
        else:
            rSP1 = force.rSP1
            rSP2 = force.rSP2
        if force.type == 'Bushing':
            F1, M1, F2, M2 = bushing_force(K=force.K,
                                           D=force.D,
                                           Kr=force.Kr,
                                           Dr=force.Dr,
                                           q1=q1,
                                           q2=q2,
                                           rSP1=rSP1,
                                           rSP2=rSP2,
                                           u0=force.u0,
                                           phi0=force.phi0)
        elif force.type == 'LocalBushing':
            F1, M1, F2, M2 = local_bushing_force(K=force.K,
                                                 D=force.D,
                                                 Kr=force.Kr,
                                                 Dr=force.Dr,
                                                 q1=q1,
                                                 q2=q2,
                                                 rSP1=rSP1,
                                                 rSP2=rSP2,
                                                 u0=force.u0,
                                                 phi0=force.phi0)

        else:
            F1, M1, F2, M2 = np.zeros(3), np.zeros(
                3), np.zeros(3), np.zeros(3)

        qe[posz1:posz1 + 6] = qe[posz1:posz1 + 6] + \
            np.concatenate((F1, M1))
        if not force.body2.name == 'Ground':
            qe[posz2:posz2 + 6] = qe[posz2:posz2 + 6] + \
                np.concatenate((F2, M2))

    # Friction forces
    for i in prange(0, len(frictions)):
        force = frictions[i]
        posy1 = int(force.body1.pos * 7)
        posz1 = int(force.body1.pos * 6)
        y1 = y[posy1: posy1 + 7]
        z1 = z[posz1: posz1 + 6]
        q1 = np.concatenate((y1, z1))
        if force.body2.name == 'Ground':
            q2 = force.body2.q0
        else:
            posy2 = int(force.body2.pos * 7)
            posz2 = int(force.body2.pos * 6)
            y2 = y[posy2: posy2 + 7]
            z2 = z[posz2: posz2 + 6]
            q2 = np.concatenate((y2, z2))

        if force.name == 'Move':
            rSP1 = force.rSP1
            rSP2 = move(t)
        else:
            rSP1 = force.rSP1
            rSP2 = force.rSP2

        if force.type == 'Friction':
            F1, M1, F2, M2 = friction_force(mud=force.mud,
                                            vd=force.vd,
                                            Fn=force.Fn,
                                            n2=force.n2,
                                            q1=q1,
                                            q2=q2,
                                            rSP1=rSP1,
                                            rSP2=rSP2)
        else:
            F1, M1, F2, M2 = np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)

        qe[posz1:posz1 + 6] = qe[posz1:posz1 + 6] + np.concatenate((F1, M1))
        if not force.body2.name == 'Ground':
            qe[posz2:posz2 + 6] = qe[posz2:posz2 + 6] + \
                np.concatenate((F2, M2))
    return qe


# @njit(cache=True)
def constraint_force_velocity(t, y, z, bodies, joints, prismatics, M, qe):
    Jg, Jgpz = jacobi_constraint(y, z, joints, prismatics)
    la, mue = lagrange_multiplicators(z, Jg, Jgpz, M, qe)
    con_force = np.dot(Jg.T, la)
    con_z = np.dot(Jg.T, mue)
    return con_force, con_z


# @njit(cache=True)
def gravitation_forces(bodies):
    qg = np.zeros(len(bodies) * 6)
    for i in prange(0, len(bodies)):
        body = bodies[i]
        posf = int(body.pos * 6)
        qg[posf:posf + 3] = body.gravitation
    return qg


# @njit(cache=True)
def spin_angular_momentum(y, z, bodies):
    qs = np.zeros(len(bodies) * 6)
    for i in prange(0, len(bodies)):
        body = bodies[i]
        posy = int(body.pos * 7)
        posz = int(body.pos * 6)
        om0KK = z[posz + 3: posz + 6]
        Ms = -np.cross(om0KK, np.dot(body.T, om0KK))
        qs[posz + 3:posz + 6] = Ms
    return qs


# @njit(cache=True)
def kinematic_ode(y, z, bodies):
    yp = np.zeros(len(bodies) * 7)
    for i in prange(0, len(bodies)):
        body = bodies[i]
        pos = body.pos
        posy = int(pos * 7)
        posz = int(pos * 6)
        pE = y[posy + 3: posy + 7]
        pEn = pE / np.linalg.norm(pE)
        v0S0 = z[posz:posz + 3]
        om0KK = z[posz + 3:posz + 6]
        _, _, L = rotation_matrix(pE)
        pEp = 0.5 * np.dot(L.T, om0KK) + np.linalg.norm(om0KK) * (pEn - pE)
        yp[posy:posy + 7] = np.concatenate((v0S0, pEp))
    return yp


# @njit(cache=True)
def rotation_matrix(pE):
    e0, e1, e2, e3 = pE
    G = np.array(
        [[-e1, e0, -e3, e2], [-e2, e3, e0, -e1], [-e3, -e2, e1, e0]])
    L = np.array(
        [[-e1, e0, e3, -e2], [-e2, -e3, e0, e1], [-e3, e2, -e1, e0]])
    A0K = np.dot(G, L.transpose())
    return A0K, G, L

############################
##         Forces         ##
############################


# @njit(cache=True)
def bushing_force(K, D, Kr, Dr, q1, q2, rSP1, rSP2, u0, phi0):
    # Location
    r010 = q1[0:3]
    r020 = q2[0:3]

    # Rotation Matrix
    A01, _, _ = rotation_matrix(q1[3:7])
    A02, _, _ = rotation_matrix(q2[3:7])

    # Velocity
    v010 = q1[7:10]
    v020 = q2[7:10]
    om011 = q1[10:13]
    om022 = q2[10:13]

    # location of connection points
    rSP10 = np.dot(A01, rSP1)
    rSP20 = np.dot(A02, rSP2)
    r0P10 = r010 + rSP10
    r0P20 = r020 + rSP20

    # velocitiy of connection points
    v01P0 = v010 + np.cross(np.dot(A01, om011), np.dot(A01, rSP1))
    v02P0 = v020 + np.cross(np.dot(A02, om022), np.dot(A02, rSP2))

    # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
    # in Kardan-Angles
    kardan_12 = kardan_diff(A01, A02)

    # Forces (Stiffness and Damping)
    dx = (r0P10 - r0P20) - u0
    dv = v01P0 - v02P0
    dom = np.dot(A01, om011) - np.dot(A02, om022)
    F1 = -np.dot(K, dx) - np.dot(D, dv)
    F2 = -F1

    # Moments (Stiffness, Damping)
    M1 = np.dot(A01.T, np.cross(rSP10, F1) - np.dot(Dr, dom) +
                np.dot(Kr, kardan_12 - phi0))
    M2 = np.dot(A02.T, np.cross(rSP20, F2) + np.dot(Dr, dom) -
                np.dot(Kr, kardan_12 - phi0))

    return F1, M1, F2, M2


# @njit(cache=True)
def local_bushing_force(K, D, Kr, Dr, q1, q2, rSP1, rSP2, u0, phi0):
    # Location
    r010 = q1[0:3]
    r020 = q2[0:3]

    # Rotation Matrix
    A01, _, _ = rotation_matrix(q1[3:7])
    A02, _, _ = rotation_matrix(q2[3:7])

    # Velocity
    v010 = q1[7:10]
    v020 = q2[7:10]
    om011 = q1[10:13]
    om022 = q2[10:13]

    # location of connection points
    rSP10 = np.dot(A01, rSP1)
    rSP20 = np.dot(A02, rSP2)
    r0P10 = r010 + rSP10
    r0P20 = r020 + rSP20
    r120 = r0P10 - r0P20
    r121 = np.dot(A01.T, r120)

    # velocitiy of connection points
    v01P0 = v010 + np.cross(np.dot(A01, om011), np.dot(A01, rSP1))
    v02P0 = v020 + np.cross(np.dot(A02, om022), np.dot(A02, rSP2))
    v120 = v01P0 - v02P0
    v121 = np.dot(A01.T, v120)

    # linearized angles between bodys, small angle approximation: cos(phi) -> 1, sin(phi) -> phi
    # in Kardan-Angles
    kardan_12 = kardan_diff(A01, A02)

    # Forces (Stiffness and Damping)
    dx = r121 - u0
    dv = v121
    dom = np.dot(A01, om011) - np.dot(A02, om022)
    F11 = -np.dot(K, dx) - np.dot(D, dv)
    F22 = -F11

    F1 = np.dot(A01, F11)
    F2 = np.dot(A01, F22)

    # Moments (Stiffness, Damping)
    M1 = np.dot(A01.T, np.cross(rSP10, F1) - np.dot(Dr, dom) +
                np.dot(Kr, kardan_12 - phi0))
    M2 = np.dot(A02.T, np.cross(rSP20, F2) + np.dot(Dr, dom) -
                np.dot(Kr, kardan_12 - phi0))
    # M1 = np.zeros(3)
    # M2 = np.zeros(3)

    return F1, M1, F2, M2


# @njit(cache=True)
def friction_force(mud, vd, Fn, n2, q1, q2, rSP1, rSP2):
    # Rotation Matrix
    A01, _, L1 = rotation_matrix(q1[3:7])
    A02, _, L2 = rotation_matrix(q2[3:7])

    # Point locations
    r1P0 = np.dot(A01, rSP1)
    r2P0 = np.dot(A02, rSP2)

    # get current gap and velocity
    vt, et = get_velocity_tangential(A01, A02, L1, L2, q1, q2, rSP1, rSP2, n2)
    Ft = get_friction_force(Fn, vt, mud, vd)
    F = Ft * et

    # forces and moments acting on bodies
    F1 = -np.dot(A02, F)
    F2 = -F1
    M1 = np.dot(A01.T, np.cross(r1P0, F1))
    M2 = np.dot(A02.T, np.cross(r2P0, F2))

    return F1, M1, F2, M2


# @njit(cache=True)
def get_friction_force(Fn, vt, mud, vd):
    # absolute tangential velocity
    vtabs = np.linalg.norm(vt)

    # linear Friction force when 0<v<vd
    if vtabs < vd:
        Ft = mud * vtabs * Fn / vd
    else:
        Ft = mud * Fn

    return Ft


# @njit(cache=True)
def get_velocity_tangential(A01, A02, L1, L2, q1, q2, rSP1, rSP2, n2):
        # location of bodies
    r010 = q1[0:3]
    r020 = q2[0:3]

    # velocities of bodies
    v010 = q1[7:10]
    v020 = q2[7:10]

    # derivation of rotation matrices
    A01d = derivation_rotation_matrix(L1, q1[10:13])
    A02d = derivation_rotation_matrix(L2, q2[10:13])

    # Velocity Vector betwwen Contact Points
    d0d = v010 + np.dot(A01d, rSP1) - v020 - np.dot(A02d, rSP2)

    # Transform to plane coordinate system
    d2d = np.dot(A02.T, d0d)

    # Perpendicular Vector to plane
    v = np.dot(d2d.T, n2)

    # Tangential velocity
    vt2 = d2d - v * n2
    vt2n = np.linalg.norm(vt2)

    # Tangential direction
    if vt2n != 0:
        et2 = vt2 / vt2n
    else:
        et2 = np.zeros(3)

    return vt2, et2


# @njit(cache=True)
def derivation_rotation_matrix(L, om0KK):
    pEp = 0.5 * np.dot(L.transpose(), om0KK)
    _, Gp, _ = rotation_matrix(pEp)
    A0Kd = 2 * np.dot(Gp, L.transpose())
    return A0Kd


# @njit(cache=True)
def kardan_diff(A01, A02):
    A12 = np.dot(A01.T, A02)
    ga_12 = -A12[0, 1]
    be_12 = A12[0, 2]
    al_12 = -A12[1, 2]
    return np.array([al_12, be_12, ga_12])

############################
##      Constraints       ##
############################


# @njit(cache=True)
def jacobi_constraint(y, z, joints, prismatics):
    dof = 0
    for joint in joints:
        dof += 3
    for prismatic in prismatics:
        dof += 5
    Jg = np.zeros((dof, len(z)))
    Jgpz = np.zeros(dof)
    j = 0
    for i in prange(0, len(joints)):
        joint = joints[i]
        posy1 = int(joint.body1.pos * 7)
        posz1 = int(joint.body1.pos * 6)
        y1 = y[posy1: posy1 + 7]
        z1 = z[posz1: posz1 + 6]
        q1 = np.concatenate((y1, z1))
        if joint.body2.name == 'Ground':
            q2 = joint.body2.q0
        else:
            posy2 = int(joint.body2.pos * 7)
            posz2 = int(joint.body2.pos * 6)
            y2 = y[posy2: posy2 + 7]
            z2 = z[posz2: posz2 + 6]
            q2 = np.concatenate((y2, z2))

        if joint.type == 'Joint':
            rSP1 = joint.rSP1
            rSP2 = joint.rSP2
            Jg1, Jg2 = joint_jacobian(q1, q2, rSP1, rSP2)
            Jg[j:j + 3, posz1:posz1 + 6] = Jg1
            if not joint.body2.name == 'Ground':
                Jg[j:j + 3, posz2:posz2 + 6] = Jg2

            Jgpz[j:j + 3] = joint_djacobian_dz(q1, q2, rSP1, rSP2)
            j += 3

    for i in prange(0, len(prismatics)):
        joint = prismatics[i]
        posy1 = int(joint.body1.pos * 7)
        posz1 = int(joint.body1.pos * 6)
        y1 = y[posy1: posy1 + 7]
        z1 = z[posz1: posz1 + 6]
        q1 = np.concatenate((y1, z1))
        if joint.body2.name == 'Ground':
            q2 = joint.body2.q0
        else:
            posy2 = int(joint.body2.pos * 7)
            posz2 = int(joint.body2.pos * 6)
            y2 = y[posy2: posy2 + 7]
            z2 = z[posz2: posz2 + 6]
            q2 = np.concatenate((y2, z2))

        if joint.type == 'Prismatic':
            rSP1 = joint.rSP1
            rSP2 = joint.rSP2
            p11 = joint.p11
            p21 = joint.p21
            Jg1, Jg2 = prismatic_jacobian(q1, q2, p11, p21, rSP1, rSP2)
            Jg[j:j + 5, posz1:posz1 + 6] = Jg1
            if not joint.body2.name == 'Ground':
                Jg[j:j + 5, posz2:posz2 + 6] = Jg2

            Jgpz[j:j +
                 5] = prismatic_djacobian_dz(q1, q2, p11, p21, rSP1, rSP2)
            j += 5

    return Jg, Jgpz


# @njit(cache=True)
def lagrange_multiplicators(z, Jg, Jgpz, M, qe):
    T1 = np.dot(Jg, np.linalg.solve(M, Jg.T))
    T2 = -Jgpz + np.dot(Jg, np.linalg.solve(M, qe))
    la = -np.linalg.solve(T1, T2)
    mue = -np.linalg.solve(np.dot(Jg, Jg.T), np.dot(Jg, z))
    return la, mue


# @njit(cache=True)
def joint_jacobian(q1, q2, rSP1, rSP2):
    # Euler Parameter
    pE1 = q1[3:7]
    pE2 = q2[3:7]

    Jg1 = np.zeros((3, 6))
    Jg2 = np.zeros((3, 6))
    E = np.identity(3)

    # Rotation Matrix
    A01, _, _ = rotation_matrix(pE1)
    A02, _, _ = rotation_matrix(pE2)

    Jg1[:, 0:3] = E
    Jg1[:, 3:6] = np.dot(A01, tilde(rSP1).T)
    Jg2[:, 0:3] = -E
    Jg2[:, 3:6] = -np.dot(A02, tilde(rSP2).T)
    return Jg1, Jg2


# @njit(cache=True)
def joint_djacobian_dz(q1, q2, rSP1, rSP2):
    # Euler Parameter
    pE1 = q1[3:7]
    pE2 = q2[3:7]

    # Rotation Matrix
    A01, _, _ = rotation_matrix(pE1)
    A02, _, _ = rotation_matrix(pE2)

    # Angular velocity
    om011 = q1[10:13]
    om022 = q2[10:13]

    return np.dot(A02, (np.cross(om022, np.cross(om022, rSP2)))) -\
        np.dot(A01, (np.cross(om011, np.cross(om011, rSP1))))


# @njit(cache=True)
def prismatic_jacobian(q1, q2, p11, p21, rSP1, rSP2):
    # State
    pE1 = q1[3:7]
    pE2 = q2[3:7]
    r010 = q1[0:3]
    r020 = q2[0:3]

    # Rotation Matrix
    A01, _, _ = rotation_matrix(pE1)
    A02, _, _ = rotation_matrix(pE2)

    # Unit arrays
    ex = np.array([1, 0, 0], dtype=np.float64)
    ey = np.array([0, 1, 0], dtype=np.float64)
    ez = np.array([0, 0, 1], dtype=np.float64)
    ex10 = np.dot(A01, ex)
    ey10 = np.dot(A01, ey)
    ez10 = np.dot(A01, ez)
    ex20 = np.dot(A02, ex)
    ey20 = np.dot(A02, ey)
    ez20 = np.dot(A02, ez)

    # Global perpendicular arrays
    p10 = np.dot(A01, p11)
    p20 = np.dot(A01, p21)

    # Connection array
    r120 = r020 + np.dot(A02, rSP2) - r010 - np.dot(A01, rSP1)

    # Two connection constraints
    Jg1 = np.zeros((5, 6))
    Jg2 = np.zeros((5, 6))
    Jg1[0, 0:3] = -p10.T
    Jg1[0, 3:6] = -np.dot(r120.T, np.dot(tilde(p10), A01))
    Jg1[1, 0:3] = -p20.T
    Jg1[1, 3:6] = -np.dot(r120.T, np.dot(tilde(p20), A01))

    Jg2[0, 0:3] = p10.T
    Jg2[1, 0:3] = p20.T

    # Three perpendicular constraints
    Jg1[2, 3:6] = -np.dot(ey20.T, np.dot(tilde(ex10), A01))
    Jg1[3, 3:6] = -np.dot(ez20.T, np.dot(tilde(ey10), A01))
    Jg1[4, 3:6] = -np.dot(ex20.T, np.dot(tilde(ez10), A01))

    Jg2[2, 3:6] = -np.dot(ex10.T, np.dot(tilde(ey20), A02))
    Jg2[3, 3:6] = -np.dot(ey10.T, np.dot(tilde(ez20), A02))
    Jg2[4, 3:6] = -np.dot(ez10.T, np.dot(tilde(ex20), A02))

    return Jg1, Jg2


# @njit(cache=True)
def prismatic_djacobian_dz(q1, q2, p11, p21, rSP1, rSP2):
    # State
    pE1 = q1[3:7]
    pE2 = q2[3:7]
    r010 = q1[0:3]
    r020 = q2[0:3]
    v010 = q1[7:10]
    v020 = q2[7:10]
    om011 = q1[10:13]
    om022 = q2[10:13]

    # Rotation Matrix
    A01, _, L1 = rotation_matrix(pE1)
    A02, _, L2 = rotation_matrix(pE2)
    A01d = derivation_rotation_matrix(L1, om011)
    A02d = derivation_rotation_matrix(L2, om022)

    # Unit arrays
    ex = np.array([1, 0, 0], dtype=np.float64)
    ey = np.array([0, 1, 0], dtype=np.float64)
    ez = np.array([0, 0, 1], dtype=np.float64)
    ex10 = np.dot(A01, ex)
    ey10 = np.dot(A01, ey)
    ez10 = np.dot(A01, ez)
    ex20 = np.dot(A02, ex)
    ey20 = np.dot(A02, ey)
    ez20 = np.dot(A02, ez)

    # Global perpendicular arrays
    p10 = np.dot(A01, p11)
    p20 = np.dot(A01, p21)

    # Connection array
    r120 = r020 + np.dot(A02, rSP2) - r010 - np.dot(A01, rSP1)

    # Derivative of global perpendicular arrays
    p10d = np.dot(A01d, p11)
    p20d = np.dot(A01d, p21)

    # Derivative of global unit arrays
    ex10d = np.dot(A01d, ex)
    ey10d = np.dot(A01d, ey)
    ez10d = np.dot(A01d, ez)
    ex20d = np.dot(A02d, ex)
    ey20d = np.dot(A02d, ey)
    ez20d = np.dot(A02d, ez)

    # Derivative of connection array
    r120d = v020 + np.cross(om022, rSP2) - v010 - np.cross(om011, rSP1)

    # Global angular velocities
    om010 = np.dot(A01, om011)
    om020 = np.dot(A02, om022)

    # Jgp*z
    Jgpz = np.zeros(5)
    Jgpz[0] = - np.dot(p10.T, np.dot(tilde(om010), r120d)) \
        - np.dot(r120.T, np.dot(tilde(om010), p10d)) \
        - 2 * np.dot(r120d.T, p10d)
    Jgpz[1] = - np.dot(p20.T, np.dot(tilde(om010), r120d)) \
        - np.dot(r120.T, np.dot(tilde(om010), p20d)) \
        - 2 * np.dot(r120d.T, p20d)
    Jgpz[2] = - np.dot(ex10.T, np.dot(tilde(om020), ey20d)) \
        - np.dot(ey20.T, np.dot(tilde(om010), ex10d)) \
        - 2 * np.dot(ey20d.T, ex10d)
    Jgpz[3] = - np.dot(ey10.T, np.dot(tilde(om020), ez20d)) \
        - np.dot(ez20.T, np.dot(tilde(om010), ey10d)) \
        - 2 * np.dot(ez20d.T, ey10d)
    Jgpz[4] = - np.dot(ez10.T, np.dot(tilde(om020), ex20d)) \
        - np.dot(ex20.T, np.dot(tilde(om010), ez10d)) \
        - 2 * np.dot(ex20d.T, ez10d)

    return Jgpz


# @njit(cache=True)
def tilde(vec):
    return np.array([[0, -vec[2], vec[1]], [vec[2], 0, -vec[0]], [-vec[1], vec[0], 0]])


def moment_of_inertia(mass, dim):
    x, y, z = dim
    return 1 / 12 * mass * np.array([[y ** 2 + z ** 2, 0, 0],
                                     [0, z ** 2 + x ** 2, 0],
                                     [0, 0, x ** 2 + y ** 2]])


def euler_to_quaternion(euler):
    roll, pitch, yaw = euler
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return np.array([qw, qx, qy, qz])


def evaluate_external_forces(t, q, bodies, force):
    # Position and Velocity
    y = q[0:int(len(bodies) * 7)]
    z = q[int(len(bodies) * 7):]
    qe = np.zeros(len(bodies) * 6)
    posy1 = int(force.body1.pos * 7)
    posz1 = int(force.body1.pos * 6)
    y1 = y[posy1: posy1 + 7]
    z1 = z[posz1: posz1 + 6]
    q1 = np.concatenate((y1, z1))
    if force.body2.name == 'Ground':
        q2 = force.body2.q0
    else:
        posy2 = int(force.body2.pos * 7)
        posz2 = int(force.body2.pos * 6)
        y2 = y[posy2: posy2 + 7]
        z2 = z[posz2: posz2 + 6]
        q2 = np.concatenate((y2, z2))

    if force.name == 'Move':
        rSP1 = force.rSP1
        rSP2 = move(t)
    else:
        rSP1 = force.rSP1
        rSP2 = force.rSP2
    if force.type == 'Bushing':
        F1, M1, F2, M2 = bushing_force(K=force.K,
                                       D=force.D,
                                       Kr=force.Kr,
                                       Dr=force.Dr,
                                       q1=q1,
                                       q2=q2,
                                       rSP1=rSP1,
                                       rSP2=rSP2,
                                       u0=force.u0,
                                       phi0=force.phi0)
    else:
        F1, M1, F2, M2 = np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)

    return np.concatenate((F1, M1))


def get_forces(t, Q, b, f):
    # Evaluate Forces
    F = {}
    appendix = ['_Fx', '_Fy', '_Fz', '_Mx', '_My', '_Mz']
    for force in f:
        for i in range(0, len(appendix)):
            F[force.name + appendix[i]] = []
    for i in range(0, len(t)):
        for force in f:
            col = Q[i, :]
            qe = evaluate_external_forces(t[i], col, b, force)
            for j in range(0, len(appendix)):
                F[force.name + appendix[j]].append(qe[j])
    return F


def save_data(t, Q, b, f):
    appendix = ['_x', '_y', '_z', '_pE0', '_pE1', '_pE2',
                '_pE3', '_vx', '_vy', '_vz', '_omx', '_omy', '_omz']
    Qsave = {'Time': t}
    for body in b:
        pos = body.pos
        posy = int(pos * 7)
        posz = int(pos * 6)
        Y = Q[:, posy:posy + 7]
        Z = Q[:, posz:posz + 6]
        Qb = np.hstack((Y, Z))
        for i, apx in enumerate(appendix):
            Qsave[body.name + apx] = Qb[:, i]

    forces = get_forces(t, Q, b, f)
    Qsave.update(forces)
    df = pd.DataFrame(Qsave, index=Qsave['Time'])
    df.to_csv(f'data.csv', sep=',')


def save_animation(t, Q, bodies):
    ta = np.array(t)
    qa = np.array(Q)
    Y = qa[:, 0:int(len(bodies) * 7)]

    with open('animation.bin', 'wb') as file:
        pickle.dump(ta, file)
        pickle.dump(Y, file)
        pickle.dump(bodies, file)
        pickle.dump([], file)
