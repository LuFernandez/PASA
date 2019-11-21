import numpy as np
import matplotlib.pylab as plt
import padasip as pa
import channel_simulator
import manchester_equalizer
import pandas as pd


n_filter = 4
training = 15
transmission = 100
n_bits = training + transmission
samples_per_bit = 16

sims = 100

r_tau = np.linspace(4, 15*samples_per_bit, 50)
mus = np.exp(-1/r_tau)

epsilons = [0.15]
#epsilons = np.arange(0.1, 1.01, 0.1)

# if not (len(epsilons) == 1 or len(mus) == 1):
# 	print('ahre')
# 	exit(-1)

ber = np.zeros(max(len(mus), len(epsilons)))


printing = False
for epsilon in epsilons:
	for sim in range(sims):
		printing = sim % 10 == 9
		print("sim n", sim+1)
		d = channel_simulator.generate_random_sequence(n_bits)
		u_ = channel_simulator.tx_channel(d)
		N = len(u_)

		u = np.concatenate((np.zeros(n_filter - 1), u_))

		#if len(epsilons) == 1:
		for n, mu in enumerate(mus):
			filt = pa.filters.FilterRLS(n_filter, mu=mu, eps=epsilon, w='zeros')
			log_d = np.zeros(N)
			log_y = np.zeros(N)

			for k in range(samples_per_bit*training):
				# measure input
				x = u[k:k + n_filter]
				# predict new value
				log_y[k] = filt.predict(x)
				# update filter
				filt.adapt(d[k], x)

			k = samples_per_bit*training
			detected = manchester_equalizer.decision_algorithm(log_y[:samples_per_bit*training])

			for _ in range(transmission):
				y_hat = []
				for i in range(samples_per_bit):
					y_hat.append(filt.predict(u[k+i:k + n_filter + i]))

				decision = manchester_equalizer.decision_algorithm(y_hat)

				for i in range(samples_per_bit):
					x = u[k + i:k + n_filter + i]
					log_y[k + i] = filt.predict(x)
					filt.adapt(decision[i], x)

				k += samples_per_bit
				detected += decision

			bit_error_rate = manchester_equalizer.calculate_ber(d[samples_per_bit*training:], detected[samples_per_bit*training:])
			if printing and not n % 100:
				print('mu=', mu, ', ber=', bit_error_rate)
			ber[n] += bit_error_rate

			# if bit_error_rate == 0 and mu < 1:
			# 	# show results
			# 	plt.plot(u_, "orange", label="u - noisy input", alpha=0.5)
			# 	plt.plot(d, "b", label="d - target")
			# 	plt.plot(log_y, "g", label="y - output")
			# 	plt.plot(detected, 'red', label='detected bits')
			# 	plt.vlines(training * samples_per_bit, colors='red', ymin=-2, ymax=2)
			# 	plt.legend()
			# 	plt.grid(which='both')
			# 	plt.show()

	ber /= sims

	plt.plot(mus, ber)
	plt.grid(which='both')
	plt.show()

	df = pd.DataFrame(
		{
			'mu': mus,
			'ber': ber
		}
	)
	df.to_csv(path_or_buf='montecarlo_alpha=1e-2_N='+ str(n_filter) + 'epsilon='+str(epsilon)+'.csv', index=False)