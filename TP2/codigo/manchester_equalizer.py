import math


samples_per_bit = 16
baud_rate = 250

one = [-1 for _ in range(math.ceil(samples_per_bit / 2))] + [+1 for _ in range(math.floor(samples_per_bit / 2))]
zero = one[-1::-1]


def calculate_ber(x, y):
	wrong_bits = 0
	n_bits = len(x)//samples_per_bit

	for j in range(0, len(x), samples_per_bit):
		if x[j] != y[j]:
			wrong_bits += 1

	return wrong_bits / (n_bits / baud_rate)


def decision_algorithm(y):
	decision = []
	i = samples_per_bit

	while i <= len(y):
		y_hat1 = 0
		y_hat2 = 0
		for _ in range(math.ceil(samples_per_bit / 2)):
			y_hat1 += y[i-samples_per_bit]
			i += 1
		for _ in range(math.floor(samples_per_bit / 2)):
			y_hat2 += y[i-samples_per_bit]
			i += 1

		if y_hat1 < y_hat2:
			decision += one
		else:
			decision += zero

	return decision
