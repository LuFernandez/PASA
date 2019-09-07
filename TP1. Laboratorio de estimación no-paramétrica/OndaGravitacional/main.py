import h5py as h5
from scipy import signal as scsig
import numpy as np
from scipy import fftpack as scfft
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

#periodograma
#z = scfft.fft(x=strain_l1[0, len(strain_l1)//5], n=len(strain_l1)) #z es la trans de fourier compleja
#zconj = np.conj(z)
#R = z*zconj
# plt.figure(1)
# plt.loglog(f, Pxx)
# plt.ylim((10e-50, 1e-37))
# plt.xlim((20, 2000))
# plt.title("Periodograma")
# plt.grid()



# cantidad de muestras
#N = len(strain_l1)//3
N = len(strain_l1)
T = 1.0 / fs
#z = scfft.fft(x=strain_l1[0:len(strain_l1)//3], n=len(strain_l1)//3)
z = scfft.fft(x=strain_l1[0:len(strain_l1)], n=len(strain_l1))
zconj = np.conj(z)
R = z*zconj
freqs = np.fft.fftfreq(len(strain_l1))
xf = np.linspace(0.0, 1.0/(2.0*T), int(N/2))    #frecuencias

plt.loglog(xf, 2.0/N * np.abs(R[:N//2]))
plt.xlim((10, 2000))
plt.grid()
plt.title("Periodogram")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density Rx(f)")
plt.show()



#hago blackman-tukey
#out = np.correlate(a=strain_l1[0:len(strain_l1)//3], v=strain_l1[0:len(strain_l1)//3], mode="full")
#out = out[len(out)//2:]
plt.acorr(strain_l1)
scsig.windows.get_window("boxcar", len(strain_l1), fftbins=True)
plt.show()
