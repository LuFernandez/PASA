import numpy as np
import matplotlib.pyplot as plt
import math
from manchester_equalizer import equalize, decision_algorithm
import sign_sign
import sign_data
import sign_error
import channel_simulator as ch_sim


baudrate = 250
fs = 4e3
mu = 0.4
#k = 20
#Ns = list(range(1, 10)) + list(range(10, 100, 10)) + list(range(100, 1001, 100))
N = 5
ber = 0
samplesperbit = math.ceil(fs / baudrate)

delay = 2
training = 10
sims = 100

mus = np.arange(0.070, 0.61, 0.001)
ber = np.zeros(len(mus))
for sim in range(sims):
	print("simulacion n ", sim+1)
	bits = np.random.randint(0, 2, 100 + training)
	tf = len(bits) / baudrate

	t = np.linspace(0, tf, math.ceil(tf * fs))
	x = []

	for bit in bits:
		if bit:
			x += [+1 for _ in range(samplesperbit // 2)]
			x += [-1 for _ in range(samplesperbit // 2)]
		else:
			x += [-1 for _ in range(samplesperbit // 2)]
			x += [+1 for _ in range(samplesperbit // 2)]

	u_noisy = ch_sim.tx_channel(x)

	for i, mu in enumerate(mus):
		# print("simulacion n ", sim)
		# plt.plot(t, x)
		# plt.plot(t, u_noisy, alpha=0.5)

		w0 = np.zeros(N)
		if delay:
			y, _ = equalize(u=u_noisy[delay:], d=x[:training*samplesperbit], mu=mu, w0=w0, samples_per_bit=samplesperbit)
		else:
			y, _ = equalize(u=u_noisy, d=x[:training*samplesperbit], mu=mu, w0=w0, samples_per_bit=samplesperbit)

		# plt.plot(t[:len(y)], y, label='delay='+str(delay))

			# y = equalize(u=u_noisy, d=x, mu=mu, N=N, w0=w0, samples_per_bit=samplesperbit)
			# y = decision_algorithm(y, samples_per_bit=samplesperbit)
			#
		wrong_bits = 0
		y = decision_algorithm(y, 16)
		# plt.plot(t[:len(y)], y)
		for j in range(samplesperbit, min([len(x), len(y)])):
			if x[j] != y[j]:
				wrong_bits += 1

		wrong_bits /= samplesperbit
		wrong_bits = int(wrong_bits)
		biterrorrate = wrong_bits/((len(bits)-1)/baudrate)
		ber[i] += biterrorrate
		#plt.plot(t[:len(y)], y, label='delay='+str(delay))

		if i % 10 == 0:
			print("mu n =", i, "mu=", mu, ', ber= ', biterrorrate)
			#print("wrong bits: ", wrong_bits)

ber = [b/sims for b in ber]
#
# ber = [b/sims for b in ber]
plt.plot(mus[:len(ber)], ber)

#bits = np.random.randint(0, 2, 10)
# bits = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1]
# tf = len(bits)/baudrate
# samplesperbit = math.ceil(fs/baudrate)
#
# t = np.linspace(0, tf, math.ceil(tf*fs))
# x = []
# for bit in bits:
# 	if bit:
# 		x += [+1 for _ in range(samplesperbit//2)]
# 		x += [-1 for _ in range(samplesperbit//2)]
# 	else:
# 		x += [-1 for _ in range(samplesperbit//2)]
# 		x += [+1 for _ in range(samplesperbit//2)]
#
# u_noisy = ch_sim.tx_channel(x)
#
#
#plt.show()

#plt.title('NLMS, $\mu$=' + str(mu) + ', ' + str(sims*1000) + ' bits')
# plt.xlabel('Tiempo')
# plt.plot(t, x, label='entrada')
# plt.plot(t, u_noisy, label='salida')
# plt.vlines(x=t[training*samplesperbit], ymin=-5, ymax=5, colors='red')
# plt.stem(ber)
plt.grid(which='both')
# plt.legend()
plt.show()
