#periodograma
#f, Pxx = scsig.periodogram(x=strain_l1, fs=fs)
f, Pxx = scsig.periodogram(x=strain_l1, fs=fs)
plt.figure(1)
plt.loglog(f, Pxx)
plt.ylim((10e-50, 1e-37))
plt.xlim((20, 2000))
plt.title("Periodograma")
plt.grid()

#strain[star:stop]

f, Pxx = scsig.welch(x=strain_l1, window='boxcar', nperseg=len(strain_l1)//5, fs=fs)
plt.figure(2)
plt.loglog(f, Pxx)
plt.ylim((1e-45, 1e-38))
plt.xlim((20, 2000))
plt.title("Welch-Bartlet")
plt.grid()
plt.show()