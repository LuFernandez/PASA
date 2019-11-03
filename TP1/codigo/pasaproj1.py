import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import lms
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


# x = [-1 if i%16 < 8 else 1 for i in range(len(t))]
u_noisy = ch_sim.tx_channel(x)

mu = 0.00001
N = 4500
delay = 1
k = 20
w0 = np.zeros(k)
y = lms.lms_filter(u=u_noisy[:-delay], d=x[delay:], mu=mu, N=N, w0=w0)
# y = lms.lms_filter(u=u_noisy, d=x, mu=mu, N=N, w0=w0)


# plt.figure(figsize=(16, 12))
# # plt.plot(w1, label='LMS, $µ=%s$' % mu)
# # plt.plot([0, len(w1) - 1], [-a, -a], color='k', linestyle='--', linewidth=2, label='$-a=%s$' % -a)
# plt.xlabel('$n$', fontsize=14)
# plt.ylabel('$w(n)$', fontsize=14)
# plt.grid(True)
# plt.title('$w(n)$ de una realización, para diferentes valores de $µ$', fontsize=14)
# plt.legend(loc='upper right', fontsize=14)
# plt.show()

plt.plot(t, x)
plt.plot(t, u_noisy, color='purple', alpha=0.5)
# y = signal.convolve(u_noisy, w1[-1], mode='same')
plt.plot(t[len(t)-len(y):], y)
# plt.vlines(np.arange(0, tf, 1/baudrate), ymin=min(u_noisy)/2, ymax=max(u_noisy)/2, colors='red')
plt.grid()
plt.ylim(10, -10)
plt.show()
