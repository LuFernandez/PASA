from nlms import nlms, nlms_step
import numpy as np
import math


def equalize(u, d, w0, mu, samples_per_bit):
	one = [-1 for _ in range(math.ceil(samples_per_bit / 2))] + [+1 for _ in range(math.floor(samples_per_bit / 2))]
	zero = one[-1::-1]
	J = []
	k = len(w0)
	t = len(d)

	w, J = nlms(u[:t], d, w0, mu)  # training sequence
	y = []
	u_ = np.concatenate((np.zeros(k-1), u))

	for i in range(len(w)):
		y.append(np.dot(w[i], u_[i:i+k]))
	# y = decision_algorithm(y, samples_per_bit=samples_per_bit)

	i = len(w)
	while i < len(u)-k-samples_per_bit:
		w_ = w[-1]
		y_hat = []
		for j in range(samples_per_bit):
			y_hat.append(np.dot(w_, u_[i+j:i+j+k]))
		d = decision_algorithm(y_hat, samples_per_bit)
		for j in range(samples_per_bit):
			w_, _ = nlms_step(u=u_[i+j:i+j+k], d=d[j], w0=w_, mu=mu)

		w.append(w_)
		#y += d
		y += y_hat
		i += samples_per_bit

	return y, J


def decision_algorithm(y, samples_per_bit):
	decision = []
	i = samples_per_bit

	one = [-1 for _ in range(math.ceil(samples_per_bit / 2))] + [+1 for _ in range(math.floor(samples_per_bit / 2))]
	zero = one[-1::-1]
	while i <= len(y):
		y_hat1 = 0
		y_hat2 = 0
		for _ in range(math.ceil(samples_per_bit / 2)):
			y_hat1 += y[i-samples_per_bit]
			i += 1
		for _ in range(math.floor(samples_per_bit / 2)):
			y_hat2 += y[i-samples_per_bit]
			i += 1

		if y_hat1 < y_hat2:
			decision += one
		else:
			decision += zero

	return decision
