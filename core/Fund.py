class Fund:
	def __init__(self, date, value, dayRaise):
		# self.name = name
		# self.code = code
		self.date = date
		self.value = value
		self.dayRaise = dayRaise

	def __str__(self):
		return "%s %s %s" % (self.date, self.value, self.dayRaise)