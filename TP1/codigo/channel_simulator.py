import numpy as np
from scipy import signal

alpha = 0.01
noise = 0.1
samples_per_bit = 16

zero = [+1 for _ in range(samples_per_bit // 2)] + [-1 for _ in range(samples_per_bit // 2)]
one = [-1 for _ in range(samples_per_bit // 2)] + [+1 for _ in range(samples_per_bit // 2)]


def generate_random_sequence(n_bits):
	bits = np.random.randint(0, 2, n_bits)
	x = []

	for bit in bits:
		if bit:
			x += one
		else:
			x += zero

	return x


def tx_channel(x):
	freq = np.random.uniform(0., np.pi, 2)
	zi = np.zeros(4)

	y = np.zeros(len(x))
	for i, sample in enumerate(x):
		pp = np.exp(freq * 1j) * [0.9, 0.95]
		p = [pp[0], np.conj(pp[0]), pp[1], np.conj(pp[1])]
		b, a = signal.zpk2tf([], p, 1)
		y_, zi = signal.lfilter(b, a, np.array([sample]), zi=zi)
		freq += alpha * np.random.uniform(-1, 1, 2)
		y[i] = y_[0]
	return y + noise * np.random.randn(len(x))


