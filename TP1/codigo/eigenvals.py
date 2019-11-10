import channel_simulator
import numpy as np
import scipy
from matplotlib import pyplot as plt
import math
import pandas as pd


def autocorr(x):
	r = np.correlate(x, x, mode='full') / len(x)
	return r[len(r) // 2:]


sims = 5000
N = 4
samples_per_bit = 16
n_bits = math.ceil(N/samples_per_bit)
mus_max = np.zeros(sims)

for sim in range(sims):
	if not sim % 50:
		print("simulacion ", sim+1)
	x = channel_simulator.generate_random_sequence(n_bits)
	u = channel_simulator.tx_channel(x)
	r = autocorr(u[:N])
	R = scipy.linalg.toeplitz(r)
	eigvals = np.linalg.eigvals(R)
	# mus_max[sim] = max(eigvals)
	mus_max[sim] = 2 / max(eigvals)

mus_max.sort()

plt.scatter(range(sims), mus_max)
plt.grid(which='both')
plt.xlabel('Número de simulación')
plt.ylabel('$\mu$ máximo')
plt.show()

plt.hist(x=mus_max, density=True, rwidth=0.95)
plt.xlabel('$\mu$ máximo')
plt.ylabel('Frecuencia (normalizado)')
plt.grid(which='both')
plt.show()

df = pd.DataFrame(
	{
		'mu': mus_max
	}
)

df.to_csv(path_or_buf='eigvals_alpha=1e-3.csv', index=False)