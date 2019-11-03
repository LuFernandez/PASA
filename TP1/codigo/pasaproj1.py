import numpy as np
import matplotlib.pyplot as plt
import math
from manchester_equalizer import equalize
import channel_simulator as ch_sim


baudrate = 250
fs = 4e3

bits = np.random.randint(0, 2, 50)
N = len(bits)
tf = N/baudrate
samplesperbit = math.ceil(fs/baudrate)

t = np.linspace(0, tf, math.ceil(tf*fs))
x = []
for bit in bits:
	if bit:
		x += [+1 for _ in range(samplesperbit//2)]
		x += [-1 for _ in range(samplesperbit//2)]
	else:
		x += [-1 for _ in range(samplesperbit//2)]
		x += [+1 for _ in range(samplesperbit//2)]


u_noisy = ch_sim.tx_channel(x)

mu = 0.001
N = 1000
delay = 1
k = 20
w0 = np.zeros(k)
training = 20
y = equalize(u=u_noisy, d=x[:samplesperbit*training], mu=mu, N=N, w0=w0, samples_per_bit=samplesperbit)

wrong_bits = 0
for i in range(samplesperbit, min([len(x), len(y)])):
	if x[i] != y[i]:
		wrong_bits += 1
print(int(wrong_bits//samplesperbit), ' de ', len(bits)-training, ' bits mal')
plt.plot(t, x)
plt.plot(t, u_noisy, color='purple', alpha=0.5)
plt.plot(t[:len(y)], y)
plt.vlines(x=t[training*samplesperbit], ymin=-5, ymax=5, colors='red')
plt.grid()
plt.show()
