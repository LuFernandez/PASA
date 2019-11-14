import numpy as np


def nlms(u, d, w0, mu):
    k = len(w0)
    m = len(u)
    w = [w0]
    J = []

    u_ = np.concatenate((np.zeros(k-1), u))
    for i in range(m):
        w_i, J_i = nlms_step(u_[i:i+k], d[i], w[-1], mu)
        w.append(w_i)
        J.append(J_i)

    del w[0]
    return w, J


def nlms_step(u, d, w0, mu):
    w = w0  # add initial condition to output so we can iterate
    u2 = np.dot(u, u)
    muu = mu*u/(u2+0.00001)
    y = np.dot(w, u)
    e = d-y
    delta_w = muu * e
    w = w + delta_w
    J = e * e

    return w, J



