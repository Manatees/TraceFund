import conn

class Fund:
	def __init__(self, name, code, pRate, rRate):
		self.Name = name
		self.Code = code
		self.PurchaseRate = pRate
		self.RedemptionRate = rRate

	def __str__(self):
		return "%s %s" % (self.Name, self.Code)

	def dailyHistory(self, days):		
		content = conn.getData(self.Code, days)
		pd = conn.parse(content)
		p = conn.FundParser()
		p.feed(pd[0])
		for h in p.links:
			print h.date, h.value, h.dayRaise


class FundHistory:
	def __init__(self, date, value, dayRaise):
		self.date = date
		self.value = value
		self.dayRaise = dayRaise