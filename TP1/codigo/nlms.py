import numpy as np


def nlms(u, d, w0, mu, N):
    k = len(w0)
    m = len(u)
    w = []

    for i in range(0, k):
        w.append(w0)
    for i in range(k, m):
        w_i, J = nlms_step(u[i-k:i], d[i], w[i-1], mu, N)
        w.append(w_i)

    return w, J


def nlms_step(u, d, w0, mu, N):
    J = []
    w = w0  # add initial condition to output so we can iterate
    u2 = np.dot(u, u)
    muu = mu*u/(u2+0.00001)
    # for _ in range(N):
    y = np.dot(w, u)
    e = d-y
    delta_w = muu * e
    w = w + delta_w
    J.append(e * e)

    return w, J



