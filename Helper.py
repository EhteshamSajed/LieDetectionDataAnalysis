import numpy as np
from scipy  import stats
import scipy.interpolate as si

class Helper:
	@staticmethod
	def getLabel(label, classCount):
		if classCount == 3:
			if label == 0:
				return [1,0,0]
			if label == 1:
				return [0,1,0]
			if label == 2:
				return [0,0,1]
			if label == 3:
				return [0,0,1]
		elif classCount == 4:
			if label == 0:
				return [1,0,0,0]
			if label == 1:
				return [0,1,0,0]
			if label == 2:
				return [0,0,1,0]
			if label == 3:
				return [0,0,0,1]


	@staticmethod
	def bspline(self, cv, n=100, degree=3, periodic=False):
		""" Calculate n samples on a bspline

			cv :      Array ov control vertices
			n  :      Number of samples to return
			degree:   Curve degree
			periodic: True - Curve is closed
					  False - Curve is open
		"""

		# If periodic, extend the point array by count+degree+1
		cv = np.asarray(cv)
		count = len(cv)

		if periodic:
			factor, fraction = divmod(count+degree+1, count)
			cv = np.concatenate((cv,) * factor + (cv[:fraction],))
			count = len(cv)
			degree = np.clip(degree,1,degree)

		# If opened, prevent degree from exceeding count-1
		else:
			degree = np.clip(degree,1,count-1)


		# Calculate knot vector
		kv = None
		if periodic:
			kv = np.arange(0-degree,count+degree+degree-1)
		else:
			kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)

		# Calculate query range
		u = np.linspace(periodic,(count-degree),n)


		# Calculate result
		return np.array(si.splev(u, (kv,cv.T,degree))).T

	@staticmethod
	def replaceInvalidByMinimumPupilSize(data, minimumPupilSize):
		for i in range(len(data)):
			if data[i] < minimumPupilSize:
				data[i] = minimumPupilSize

		return data

	@staticmethod
	def getSlidingWindowSkewness(data, window, step):
		i = 0
		n = 0
		result = []
		while i + window < len(data):
			skewness = stats.skew(data[i:i+window])
			result.append(skewness)
			i = i + step
		return result

	@staticmethod
	def getSlidingWindowKurtosis(data, window, step):
		i = 0
		n = 0
		result = []
		while i + window < len(data):
			kurt = stats.kurtosis(data[i:i+window])
			result.append(kurt)
			i = i + step
		return result

	@staticmethod
	def getCentralBaselineMean(data):
		centralArea = data[60:-60]
		mean = sum(centralArea)/len(centralArea)
		return mean

	@staticmethod
	def getFirstMinimumValueAndIndex(data):
		minimum = min(data)
		minIndex = np.where(np.array(data) == minimum)[0][0]
		return minimum, minIndex


	@staticmethod
	def smooth(dataSet, window):
		result = []
		hand = int((window-1)/2)
		for i in range(len(dataSet)):
			if i < hand:
				mean = sum(dataSet[:i+hand+1])/(i+hand+1) 
			elif i + hand >= len(dataSet):
				mean = sum(dataSet[i-hand:])/(hand + len(dataSet) - i)
			else:
				mean = sum(dataSet[i-hand:i+hand+1])/window
			result.append(mean)
		return result

	@staticmethod
	def getWholeSkewness(dataSet, window):
		result = []
		hand = int((window-1)/2)
		for i in range(len(dataSet)):
			if i < hand:
				skew = stats.skew(dataSet[:i+hand+1])
			elif i + hand >= len(dataSet):
				skew = stats.skew(dataSet[i-hand:])
			else:
				skew = stats.skew(dataSet[i-hand:i+hand+1])
			result.append(skew)
		return result

	@staticmethod
	def getWholeKurtosis(dataSet, window):
		result = []
		hand = int((window-1)/2)
		for i in range(len(dataSet)):
			if i < hand:
				kurt = stats.kurtosis(dataSet[:i+hand+1])
			elif i + hand >= len(dataSet):
				kurt = stats.kurtosis(dataSet[i-hand:])
			else:
				kurt = stats.kurtosis(dataSet[i-hand:i+hand+1])
			result.append(kurt)
		return result

	@staticmethod
	def extendZeroZone(pplList, width):
		# for dt in data:
		# pplList = dt['pupilList']
		isZeroZone = pplList[0] == 0

		for i in range(len(pplList)):
			if not isZeroZone and pplList[i] == 0:
				isZeroZone = True
				for j in range(i-width,i):
					if j >= 0:
						pplList[j] = 0
			# if isZeroZone and pplList[i] != 0:
			# 	isZeroZone = False
			# 	for j in range(i + 1, i + width + 1):
			# 		if j < len(pplList):
			# 			pplList[j] = 0
			# 	i = i + width
		# dt['pupilList'] = pplList
		return pplList

	@staticmethod
	def replaceBlankByLinearInterpolation(data):
		# print(data[0], " cccccc")
		x1 = data[0]
		blankZone = x1 == 0
		index = 0
		for i in range(1,len(data)):
			x = data[i]
			log = ""
			if x1 != 0 and x == 0:
				log = log + " blank zone " + str(x1)
				blankZone = True
			if not blankZone and x != 0:
				x1 = x
				index = i
				log = log + " index " + str(i)

			if blankZone and x != 0:
				log = log + " blankZone stopped " + str(x1)
				blankZone = False
				if data[index] == 0:
					data[index] = x
					# print("preblank stopped at index",i)
					# plt.plot(data)
				diff = x - x1
				length = i - index
				# print("replace started")
				for j in range(index + 1, i + 1):
					if j < len(data):
						newVal = x1 + (diff / length) * (j - index)
						# print("Replacing ",j, " with ", newVal)
						data[j] = newVal
					

				x1 = x

			# print(x, log)
		if blankZone:
			for j in range(index + 1, len(data)):
				newVal = x1
				# print("Replacing ",j, " with ", newVal)
				data[j] = newVal

		return data
		