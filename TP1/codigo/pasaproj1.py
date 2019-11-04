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

mu = 0.0001
k = 20
w0 = np.zeros(k)
Ns = list(range(1, 10)) + list(range(10, 100, 10))
#Ns = [20]
ber = np.zeros(len(Ns))
sims = 5

for _ in range(sims):
	print("simulacion n ", _)
	bits = np.random.randint(0, 2, 1001)
	tf = len(bits)/baudrate
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

	for j, N in enumerate(Ns):
		y, _ = sign_sign.sign_sign_filter(u_noisy, x, w0, mu, N)
		y = decision_algorithm(y, samplesperbit)
		# plt.plot(t, x)
		# plt.plot(t, y)
		# plt.show()
		# y = equalize(u=u_noisy, d=x, mu=mu, N=N, w0=w0, samples_per_bit=samplesperbit)

		wrong_bits = 0
		for i in range(samplesperbit, min([len(x), len(y)])):
			if x[i] != y[i]:
				wrong_bits += 1

		wrong_bits /= samplesperbit
		wrong_bits = int(wrong_bits)
		biterrorrate = wrong_bits/((len(bits)-1)/baudrate)
		ber[j] += biterrorrate

		if wrong_bits == 0:
			break
		print("N=", N, ', ber= ', biterrorrate)


ber = [b/sims for b in ber]
plt.stem(Ns[:len(ber)], ber)
plt.title('NLMS, $\mu$=' + str(mu)+', M=,' + str(k) + ', ' + str(sims*1000) + ' bits')
plt.xlabel('Número de iteraciones por paso')
plt.ylabel('Bit error rate')
# plt.plot(t, u_noisy, color='purple', alpha=0.5)
# plt.plot(t[:len(y)], y)
# plt.vlines(x=t[training*samplesperbit], ymin=-5, ymax=5, colors='red')
plt.grid()
plt.show()
