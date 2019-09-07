
#hago blackman-tukey
#out = np.correlate(a=strain_l1[0:len(strain_l1)//3], v=strain_l1[0:len(strain_l1)//3], mode="full")
#out = out[len(out)//2:]
plt.acorr(strain_l1)
scsig.windows.get_window("boxcar", len(strain_l1), fftbins=True)
plt.show()
