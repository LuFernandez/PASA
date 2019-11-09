import pandas as pd
import matplotlib.pyplot as plt


N_filter = 4
delay = 1
trainings = [15, 30, 50, 75]
alpha = '1e-2'

bers = []
mus = []
for i, training in enumerate(trainings):
	path = 'montecarlo_alpha='+ alpha +'_delay=' + str(delay) +\
		   "_N=" + str(N_filter) + '_training=' + str(training) + '.csv'

	data = pd.read_csv(path)
	plt.plot(data['mu'], data['ber'], marker='o', label=str(training)+' bits de entrenamiento')

plt.grid(which='both')
plt.xlabel('Paso $\mu$')
plt.ylabel('Bit error rate')
plt.legend()
plt.show()
