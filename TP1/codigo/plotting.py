import pandas as pd
import matplotlib.pyplot as plt


Ns_filter = [4, 5, 6]
delay = 1
training = 15
alpha = '1e-3'

bers = []
mus = []

plt.figure(figsize=(5, 4))
for i, N_filter in enumerate(Ns_filter):
	path = 'montecarlo_alpha=' + alpha + '_delay=' + str(delay) +\
		   "_N=" + str(N_filter) + '_training=' + str(training) + '.csv'

	data = pd.read_csv(path)
	plt.plot(data['mu'], data['ber'], marker='o', label='N='+str(N_filter))

plt.grid(which='both')
plt.xlabel('Paso $\mu$')
plt.ylabel('Bit error rate')
#plt.xlim([0, 1])
plt.legend()
plt.show()
