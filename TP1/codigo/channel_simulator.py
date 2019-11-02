import numpy as np
from scipy import signal

alpha = 0.01
noise = 0.1

def tx_channel(x):
	y = np.array([])
	for sample in x:
		pp = np.exp(tx_channel.freq * 1j) * [0.9, 0.95]
		p = [pp[0], np.conj(pp[0]), pp[1], np.conj(pp[1])]
		b, a = signal.zpk2tf([], p, 1)
		y_, tx_channel.zi = signal.lfilter(b, a, np.array([sample]), zi=tx_channel.zi)
		tx_channel.freq += alpha * np.random.uniform(-1, 1, 2)
		y = np.append(y, y_[0])
	return y + noise * np.random.randn(len(x))


tx_channel.freq = np.random.uniform(0., np.pi, 2)
tx_channel.zi = np.zeros(4)