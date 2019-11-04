import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import time
import lms
import nlms
import sign_error
import sign_data
import sign_sign
import channel_simulator as ch_sim


baudrate = 250
fs = 4e3

bits = np.random.randint(0, 2, 1000)
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


mu = 0.0002
N = 20
delay = 1
k = 20
w0 = np.zeros(k)
#y = lms.lms_filter(u=u_noisy[:-delay], d=x[delay:], mu=mu, N=N, w0=w0)
start = time.process_time()
y, J = sign_sign.sign_sign_filter(u=u_noisy, d=x, mu=mu, N=N, w0=w0)
end = time.process_time()
print(end - start)


plt.figure()
plt.plot(J)
plt.xlabel('iteraciones')
plt.grid()
plt.show()


wrong_bits = 0
for i in range(samplesperbit, min([len(x), len(y)])):
	if x[i] != y[i]:
		wrong_bits += 1
print(int(wrong_bits//samplesperbit), ' de ', len(bits)-1, ' bits mal')
#print()

plt.figure()
plt.plot(t, x)
plt.plot(t, u_noisy, color='purple', alpha=0.1)
# y = signal.convolve(u_noisy, w1[-1], mode='same')
plt.plot(t[len(t)-len(y):], y)
# plt.vlines(np.arange(0, tf, 1/baudrate), ymin=min(u_noisy)/2, ymax=max(u_noisy)/2, colors='red')
plt.grid()
#plt.ylim(-10, 10)
plt.show()
