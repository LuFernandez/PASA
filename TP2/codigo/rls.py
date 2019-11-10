import numpy as np
import matplotlib.pylab as plt
import padasip as pa
import channel_simulator


# these two function supplement your online measurment
def measure_x():
	# it produces input vector of size 3
	x = np.random.random(3)
	return x


def measure_d(x):
	# meausure system output
	d = 2 * x[0] + 1 * x[1] - 1.5 * x[2]
	return d




N_filter = 4
training = 20
transmission = 100
n_bits = training + transmission
samples_per_bit = 16
filt = pa.filters.FilterRLS(N_filter, mu=0.98, eps=0.001, w='zeros')
d = channel_simulator.generate_random_sequence(n_bits)
u_ = channel_simulator.tx_channel(d)
N = len(u_)

u = np.concatenate((np.zeros(N_filter-1), u_))
log_d = np.zeros(N)
log_y = np.zeros(N)
for k in range(samples_per_bit*training):
	# measure input
	x = u[k:k+N_filter]
	# predict new value
	y = filt.predict(x)
	# do the important stuff with prediction output
	pass
	# measure output
	# d = measure_d(x)
	# update filter
	filt.adapt(d[k], x)
	# log values
	log_y[k] = y

k = samples_per_bit*training
detected = [0 for __ in range(k)]

for _ in range(transmission):
	y_hat = []
	for i in range(samples_per_bit):
		y_hat.append(np.dot(u[k+i:k+N_filter+i], filt.w))

	if sum(y_hat[:samples_per_bit//2]) > sum(y_hat[samples_per_bit//2:]):
		decision = [+1 for __ in range(samples_per_bit//2)] + [-1 for __ in range(samples_per_bit//2)]
	else:
		decision = [-1 for __ in range(samples_per_bit//2)] + [+1 for __ in range(samples_per_bit//2)]

	for i in range(samples_per_bit):
		x = u[k + i:k + N_filter + i]
		y = filt.predict(x)
		filt.adapt(decision[i], x)
		log_y[k+i] = y

	k += samples_per_bit
	detected += decision

# show results
plt.plot(u_, "orange", label="u - noisy input", alpha=0.5)
plt.plot(d, "b", label="d - target")
plt.plot(log_y, "g", label="y - output")
plt.plot(detected, 'red', label='detected bits')
plt.vlines(training*samples_per_bit, colors='red', ymin=-2, ymax=2)
plt.legend()
plt.grid(which='both')
plt.show()
