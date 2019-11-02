def calc_lms_montecarlo(K, mu, N, w0):
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

    for i in range(K):
        u = get_model_output(N)

        # Predicción LMS
        w = np.zeros((N, 1))
        J = np.zeros((N, 1))
        w[0] = w0

        for n in range(1, N):
            y = w[n] * u_noisy[n]
            d = u[n - delay]
            # y = w[n - 1] * u[n - 1]                 # Ecuación de filtrado
            # d = u[n]
            e = d - y
            J[n - 1] = e * e
            w[n] = w[n - 1] + mu * u[n - 1] * e  # Ecuación LMS

        J[N - 1] = J[N - 2]

        w_montecarlo += w
        J_montecarlo += J

    w_montecarlo /= K
    J_montecarlo /= K

    return (w_montecarlo, J_montecarlo)


