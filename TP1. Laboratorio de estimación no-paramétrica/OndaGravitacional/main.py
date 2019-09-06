import h5py as h5
from scipy import signal as scsig
import numpy as np
import matplotlib.pyplot as plt
import readligo as rl

fs = 4096

# leemos los datos de livingston
pathL1 = '../LIGO/L-L1_LOSC_4_V2-1126259446-32.hdf5'
strain_l1, time_l1, chan_dict_l1 = rl.loaddata(pathL1, 'L1')
dt = time_l1[1] - time_l1[0]
times = dt*np.array([i for i in range(len(strain_l1))])

# leemos los datos de hanford
pathH1 = '../LIGO/H-H1_LOSC_4_V2-1126259446-32.hdf5'
strain_h1, time_h1, chan_dict_h1 = rl.loaddata(pathH1, 'H1')
#plt.plot(times, strain_h1)
#plt.plot(times, strain_l1)
#plt.grid()
#plt.show()

# periodograma
#f, Pxx = scsig.periodogram(x=strain_l1, fs=fs)
f, Pxx = scsig.periodogram(x=strain_l1, fs=fs)
plt.figure(1)
plt.loglog(f, Pxx)
plt.ylim((10e-50, 1e-37))
plt.xlim((20, 2000))
plt.title("Periodograma")
plt.grid()

# strain[star:stop]

f, Pxx = scsig.welch(x=strain_l1, window='boxcar', nperseg=len(strain_l1)//5, fs=fs)
plt.figure(2)
plt.loglog(f, Pxx)
plt.ylim((1e-45, 1e-38))
plt.xlim((20, 2000))
plt.title("Welch-Bartlet")
plt.grid()
plt.show()
