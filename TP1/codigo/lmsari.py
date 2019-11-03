import numpy as np


def lms(u, d, mu, N):
    m = len(u)
    y = np.zeros(m)
    e = np.zeros(m)
    w = np.zeros((m, N + 1))
    n = N

    # print(m, n)

    for i in range(m):

        ### Primero actualizo w[n]

        for k in range(0, n + 1):
            if i - k - 1 >= 0:
                w[i][k] = w[i - 1][k] + mu * u[i - k - 1] * e[i - 1]  # formula de LMS
            else:
                w[i][k] = 0.001

        ### En segundo lugar actualizo la salida
        if i + 1 >= n + 1:
            y[i] = np.dot(w[i], np.flip(u[i + 1 - (n + 1):i + 1]))
        else:
            y[i] = np.dot(w[i][:i + 1], np.flip(u[:i + 1]))

        ### En tercer lugar actualizo el error

        e[i] = d[i] - y[i]

    return y, w, e






















def calc_lms_montecarlo(u, u_noisy, K, mu, N, w0, delay):
    """
    Realiza una simulación de Monte-Carlo del algoritmo LMS
    aplicado a un problema de predicción lineal de orden uno.

    K: número de simulaciones de Monte-Carlo
    mu: parámetro de paso
    N: número de iteraciones
    w0: valor inicial del filtro adaptativo
    """

    # Simulación de Monte Carlo
    w_montecarlo = np.zeros((N, 1))
    J_montecarlo = np.zeros((N, 1))

    for _ in range(K):
        # u = get_model_output(N)

        # Predicción LMS
        w = np.zeros((N+1, 1))
        J = np.zeros((N, 1))
        w[0] = w0

        for n in range(0, N):
            y = w[n] * u_noisy[n]
            d = u[n - delay]
            # y = w[n - 1] * u[n - 1]                 # Ecuación de filtrado
            # d = u[n]
            e = d - y
            J[n] = e * e
            w[n + 1] = w[n] + mu * u[n] * e  # Ecuación LMS
        w = w[:N]

        # J[N - 1] = J[N - 2]

        w_montecarlo += w
        J_montecarlo += J

    w_montecarlo /= K
    J_montecarlo /= K

    return w_montecarlo, J_montecarlo


