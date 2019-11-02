import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import lms
import channel_simulator




baudrate = 250
fs = 4e3

bits = np.random.randint(0, 2, 100)
N = len(bits)
tf = N/baudrate
samplesperbit = math.ceil(fs/baudrate)

t = np.linspace(0, tf, math.ceil(tf*fs))
x = []
for bit in bits:
	if bit:
		x += [1 for _ in range(samplesperbit//2)]
		x += [-1 for _ in range(samplesperbit//2)]
	else:
		x += [-1 for _ in range(samplesperbit//2)]
		x += [1 for _ in range(samplesperbit//2)]


# x = [-1 if i%16 < 8 else 1 for i in range(len(t))]
y = tx_channel(x)

plt.plot(t, x)
plt.plot(t, y, color='purple')
plt.vlines(np.arange(0, tf, 1/baudrate), ymin=min(y)/2, ymax=max(y)/2, colors='red')
plt.grid()
plt.show()
