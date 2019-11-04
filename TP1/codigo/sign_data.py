import numpy as np


def sign_data_filter(u, d, w0, mu, N):
	k = len(w0)
	w, J = sign_data(u, d, w0, mu, N)
	y = []
	u_ = np.concatenate((np.zeros(k), u))
	for i in range(0, len(w)):
		y.append(np.dot(w[i], u_[i:i+k]))

	return y, J


def sign_data(u, d, w0, mu, N):
	k = len(w0)
	m = len(u)
	w = []

	for i in range(0, k):
		w.append(w0)
	for i in range(k, m):
		w_i, J = sign_data_step(u[i - k:i], d[i], w[i - 1], mu, N)
		w.append(w_i)

	return w, J


def sign_data_step(u, d, w0, mu, N):
	J = []
	w = w0  # add initial condition to output so we can iterate
	# u2 = np.dot(u, u)
	for _ in range(N):
		y = np.dot(w, u)
		e = d-y
		delta_w = mu * np.sign(u) * e
		w = w + delta_w
		J.append(e * e)

	return w, J



