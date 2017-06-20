def calculateRate(rateTable, day):
	lastRate = rateTable[-1]
	for rate in rateTable[:-1]:
		if day < int(rate['day']):
			return rate['rate']			
	return lastRate['rate']