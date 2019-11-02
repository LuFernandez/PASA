import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

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

baudrate = 250
fs = 4e3

bits = np.random.randint(0, 2, 100)
N = len(bits)
tf = N/baudrate
samplesperbit = math.ceil(fs/baudrate)

t = np.linspace(0, tf, math.ceil(tf*fs))
x = []
for bit in bits:
	if bit:
		x += [1 for _ in range(samplesperbit//2)]
		x += [-1 for _ in range(samplesperbit//2)]
	else:
		x += [-1 for _ in range(samplesperbit//2)]
		x += [1 for _ in range(samplesperbit//2)]


# x = [-1 if i%16 < 8 else 1 for i in range(len(t))]
y = tx_channel(x)

plt.plot(t, x)
plt.plot(t, y, color='purple')
plt.vlines(np.arange(0, tf, 1/baudrate), ymin=min(y)/2, ymax=max(y)/2, colors='red')
plt.grid()
plt.show()
