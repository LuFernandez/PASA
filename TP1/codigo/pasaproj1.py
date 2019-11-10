import numpy as np
import matplotlib.pyplot as plt
import math
from manchester_equalizer import equalize, decision_algorithm
import sign_sign
import sign_data
import sign_error
import channel_simulator as ch_sim
import pandas as pd


baud_rate = 250
fs = 4e3
samples_per_bit = math.ceil(fs / baud_rate)

delay = 1
training = 15
sims = 100
N_bits = 100
N_filter = 4


# mus = [0.005]
# mus = np.arange(0.005, 0.1, 0.001)
# mus = np.concatenate((np.arange(0.005, 0.01, 0.001), np.arange(0.01, 0.5, 0.01)))
mus = np.concatenate((np.arange(0.0001, 0.01, 0.0002), np.arange(0.01, 1, 0.01)))
ber = np.zeros(len(mus))
# energies = np.zeros(sims)

for sim in range(sims):
	x = ch_sim.generate_random_sequence(N_bits+training)
	# tf = (N_bits + training) / baud_rate
	# t = np.linspace(0, tf, math.ceil(tf * fs))

	u_noisy = ch_sim.tx_channel(x)
	# diff = np.diff(u_noisy)
	# energies[sim] = np.dot(diff, diff)

	print("simulacion n ", sim+1)

	for i, mu in enumerate(mus):
		# plt.plot(t, x)
		# plt.plot(t, u_noisy, alpha=0.5)

		w0 = np.zeros(N_filter)
		if delay:
			y, J = equalize(u=u_noisy[delay:], d=x[:training * samples_per_bit], mu=mu, w0=w0, samples_per_bit=samples_per_bit)
		else:
			y, J = equalize(u=u_noisy, d=x[:training * samples_per_bit], mu=mu, w0=w0, samples_per_bit=samples_per_bit)

		# plt.plot(t[:len(y)], y, label='delay='+str(delay))

		wrong_bits = 0
		y_d = decision_algorithm(y, samples_per_bit)
		# plt.plot(t[:len(y)], y)
		for j in range(samples_per_bit*training, min([len(x), len(y_d)]), samples_per_bit):
			if x[j] != y_d[j]:
				wrong_bits += 1

		biterrorrate = wrong_bits/(N_bits / baud_rate)
		ber[i] += biterrorrate

		# plt.plot(t[:len(J)], J)

		if i % 10 == 0:
			print("mu n =", i, "mu=", mu, ', ber= ', biterrorrate)
			# print("wrong bits: ", wrong_bits)

		# if biterrorrate >= 0:
		# 	plt.plot(t, x)
		# 	plt.plot(t[:len(y)], y)
		# 	plt.plot(t[:len(y_d)], y_d)
		# 	plt.plot(t[:len(u_noisy)], u_noisy, alpha=0.5, color='black')
		# 	plt.grid(which='both')
		# 	plt.show()

# ber = [b/len(mus) for b in ber]
# Js = [J/sims for J in Js]
#
ber = [b/sims for b in ber]
plt.plot(mus, ber)
plt.grid(which='both')
plt.show()





# plt.title('NLMS, $\mu$=' + str(mu) + ', ' + str(sims*1000) + ' bits')
# plt.xlabel('Tiempo')
# plt.plot(t, x, label='entrada')
# plt.plot(t, u_noisy, label='salida')
# plt.vlines(x=t[training*samplesperbit], ymin=-5, ymax=5, colors='red')
# plt.stem(ber)


# df = pd.DataFrame(
# 	{
# 		'mu': mus,
# 		'ber': ber
# 	}
# )
#
# df.to_csv(path_or_buf='montecarlo_alpha=1e-2_delay='+str(delay)+
# 					  '_N='+str(N_filter)+'_training='+str(training)+'.csv', index=False)

df = pd.DataFrame(
	{
		'mu': mus,
		'ber': ber
	}
)

df.to_csv(path_or_buf='montecarlo_alpha=1e-3_delay='+str(delay)+
					  '_N='+str(N_filter)+'_training='+str(training)+'.csv', index=False)