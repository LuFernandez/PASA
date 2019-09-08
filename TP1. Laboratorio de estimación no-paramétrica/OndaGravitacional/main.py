import numpy as np
from scipy import signal as scsig

# hago blackman-tukey
# out = np.correlate(a=strain_l1[0:len(strain_l1)//3], v=strain_l1[0:len(strain_l1)//3], mode="full")
# out = out[len(out)//2:]
# plt.acorr(strain_l1)
# scsig.windows.get_window("boxcar", len(strain_l1), fftbins=True)
# plt.show()

# nperseg : L



fs = nfft = nperseg = 512
t = np.arange(8192) / fs
x = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*100*t) + np.sin(2*np.pi*150*t)

welch_barlett(data=x, fs=fs, title='', D=2, nperseg=512, nfft=512)
