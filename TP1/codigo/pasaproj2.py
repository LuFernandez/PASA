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
from manchester_equalizer import decision_algorithm, equalize


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



# mu = np.float_power(2, -10)
mu = 0.005
N = 500
delay = 1
k = 20
w0 = np.zeros(k)
monticharles = 10
J = []
total_time = 0.0
#y = lms.lms_filter(u=u_noisy[:-delay], d=x[delay:], mu=mu, N=N, w0=w0)
# start = time.process_time()
# y, J = sign_sign.sign_sign_filter(u=u_noisy, d=x, mu=mu, N=N, w0=w0)
# end = time.process_time()
# # output = decision_algorithm(y, samplesperbit)
# print(end - start)


plt.figure()
for i in range(monticharles):
	u_noisy = ch_sim.tx_channel(x)
	start = time.process_time()
	# y, J_i = equalize(u=u_noisy,d=x,mu=mu, N=N,w0=w0,samples_per_bit=samplesperbit)
	y, J_i = lms.lms_filter(u=u_noisy, d=x, w0=w0, N=N, mu=mu)
	end = time.process_time()
	total_time += end-start
	plt.plot(J_i)
	print(i)
print(total_time/monticharles)
plt.title('Montecarlo nlms')
plt.xlabel('$N$')
plt.ylabel('$J(N)$')
# plt.ylim([-0.01, .2])
plt.grid()
plt.show()


# plt.figure()
# plt.title('Cost function')
# plt.plot(J_lms, linewidth=1.5)
# plt.plot(J_nlms, linewidth=1.5)
# plt.plot(J_error, linewidth=1.5)
# plt.plot(J_data, linewidth=1.5)
# plt.plot(J_sign, linewidth=1.5)
# plt.legend(['LMS', 'NLMS', 'sign-error', 'sign-data', 'sign-sign'])
# plt.xlabel('$N$')
# plt.ylabel('$J(N)$')
# plt.grid()
# plt.show()

# plt.figure()
# plt.plot(t, x)
# plt.plot(t, u_noisy, color='purple', alpha=0.1)
# # y = signal.convolve(u_noisy, w1[-1], mode='same')
# plt.plot(t[len(t)-len(y):], y)
# # plt.vlines(np.arange(0, tf, 1/baudrate), ymin=min(u_noisy)/2, ymax=max(u_noisy)/2, colors='red')
# plt.grid()
# #plt.ylim(-10, 10)
# plt.show()
# wrong_bits = 0
# for i in range(samplesperbit, min([len(x), len(y)])):
# 	if x[i] != y[i]:
# 		wrong_bits += 1
# print(int(wrong_bits//samplesperbit), ' de ', len(bits)-1, ' bits mal')
# #print()
#
# plt.figure()
# plt.plot(t, x)
# plt.plot(t, u_noisy, color='purple', alpha=0.1)
# # y = signal.convolve(u_noisy, w1[-1], mode='same')
# plt.plot(t[len(t)-len(y):], y)
# # plt.vlines(np.arange(0, tf, 1/baudrate), ymin=min(u_noisy)/2, ymax=max(u_noisy)/2, colors='red')
# plt.grid()
# #plt.ylim(-10, 10)
# plt.show()
# >>>>>>> 956f7506fe893379e2413ec9f93cdf8edb71cd8a
