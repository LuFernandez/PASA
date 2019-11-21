import pandas as pd
import matplotlib.pyplot as plt


epsilons = [0.1, 0.15, 0.2, 0.5, 1]
# epsilons = [0.1, 0.15, 0.2, 0.5, 1]
alpha = '1e-2'
n_filter = 6

bers = []
mus = []

plt.figure(figsize=(5, 4))
for i, epsilon in enumerate(epsilons):
	# path = 'montecarlo_alpha=1e-2_epsilon='+str(epsilon)+'.csv'
	path = 'montecarlo_alpha=1e-2_N=' + str(n_filter) + 'epsilon='+str(epsilon)+'.csv'
	data = pd.read_csv(path)
	plt.plot(data['mu'], data['ber'], marker='o', label='$\delta$='+str(epsilon))

plt.grid(which='both')
plt.xlabel('$\lambda$')
plt.ylabel('Bit error rate')
plt.ylim([0, 11])
plt.legend()
plt.show()