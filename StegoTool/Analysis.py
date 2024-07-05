from math import ceil, pow, log2, log, sqrt

def ChiSquare(bitstream, size, nmemb):
	bitstream += '0'
	nums = [int(bitstream[i * size : (i + 1) * size], 2) for i in range(nmemb)]

	M = int(pow(2, ceil(log2(size))))
	P = pow(2, size) / M
	E = nmemb / M
	O = [0 for i in range(M)]

	# Classification
	for i in range(nmemb):
		for j in range(M):
			if(P * j <= nums[i] and nums[i] < P * (j + 1)):
				O[j] += 1
				break

	# Chi-square test
	chi = 0.0
	for i in range(M):
		chi += pow(float(O[i]) - E, 2) / E

	return chi

def CalculateRS(nums, start, end):
	n = end - start
	Y = [0.0 for i in range(n)]
	Z = [0.0 for i in range(n)]

	M = sum(nums[start:end]) / n

	for i in range(n):
		Y[i] = nums[start + i] - M

	Z[0] = Y[0]
	for i in range(1, n):
		Z[i] = Z[i - 1] + Y[i]

	R = max(Z) - min(Z)
	S = sqrt(sum([pow(nums[i], 2) for i in range(start, end)]) / n - pow(M, 2))

	return R / S

def Slope(nPoint, logN, logRS):
	sumX = sum(logN)
	sumY = sum(logRS)
	sumXY = sum([logN[i] * logRS[i] for i in range(len(logN))])
	sumXX = sum([logN[i] * logN[i] for i in range(len(logN))])

	return (nPoint * sumXY - sumX * sumY) / (nPoint * sumXX - sumX * sumY)

def RS(bitstream, size, nmemb):
	bitstream += '0'
	nums = [int(bitstream[i * size : (i + 1) * size], 2) for i in range(nmemb)]

	windowCtg = int(log2(nmemb)) - 1
	logN = [0.0 for i in range(windowCtg)]
	logRS = [0.0 for i in range(windowCtg)]

	window_num = 1
	for i in range(windowCtg):
		sum_RS = 0.0
		window_size = int(nmemb / window_num)

		for j in range(window_size):
			sum_RS += CalculateRS(nums, j * window_size, (j + 1) * window_size)

		average_RS = sum_RS / window_num
		logRS[i] = log(average_RS)
		logN[i] = log(window_size)

		window_num *= 2

	return Slope(windowCtg, logN, logRS)