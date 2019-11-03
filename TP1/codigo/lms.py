import numpy as np


def lms_filter(u, d, w0, mu, N):
    k = len(w0)
    w = lms(u, d, w0, mu, N)
    y = []
    u_ = np.concatenate((np.zeros(k), u))
    for i in range(0, len(w)):
        y.append(np.dot(w[i], u_[i:i+k]))

    return y


def lms(u, d, w0, mu, N):
    k = len(w0)
    m = len(u)
    w = []

    for i in range(0, k):
        w.append(w0)
    for i in range(k, m):
        w.append(lms_step(u[i-k:i], d[i], w[i-1], mu, N))

    return w


def lms_step(u, d, w0, mu, N):

    w = w0  # add initial condition to output so we can iterate
    # u2 = np.dot(u, u)
    muu = mu*u
    for _ in range(N):
        y = np.dot(w, u)
        e = d-y
        delta_w = muu * e
        w = w + delta_w

    return w



