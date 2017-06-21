import json
import conn
import Fund



class Account:
	def __init__(self):
		self.name = ""
		self.code = 0
		self.purchaseRate = 0
		self.redemptionRate = []

	def setup(self):
		config = open('Fund.conf')
		jsonData = json.load(config)
		config.close()

		self.HoldFunds = []
		for fundKey in jsonData.keys():			
			n = jsonData[fundKey]["name"]
			c = jsonData[fundKey]["code"]
			p = jsonData[fundKey]["purchaseRate"]
			r = jsonData[fundKey]["redemptionRate"]
			f = Fund.Fund(n,c,p,r)
			self.HoldFunds.append(f)
