from django.db import models
from . import utilities

class Fund(models.Model):
	fund_name = models.CharField(max_length=200)
	fund_code = models.CharField(max_length=20)
	fund_p_rate = models.DecimalField('purchase rate', max_digits=4, decimal_places=4)
	

	def __str__(self):
		return '%s (%s)' % (self.fund_name, self.fund_code)

	def latest_fund_data(self):		
		return self.fundhistory_set.order_by('-date')[0]

	def __refresh_fund_data(self, in_days):
		return utilities.do_it(self.fund_code, in_days)

	def update(self):
		self.latest_remote_fund_data = self.__refresh_fund_data(1)


class FundHistory(models.Model):
	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	date = models.DateField('history date')
	netprice = models.DecimalField('net price', max_digits=4, decimal_places=4)
	note = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return '%s -> %g, %s' % (self.fund.fund_name, self.netprice, self.date)

class RedemptionRateTable(models.Model):
	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	days = models.IntegerField('in thers days', default=0)
	rate_value = models.DecimalField(max_digits=4, decimal_places=4, default=0)

	def __str__(self):
		return '%s -> %d: %g' % ( self.fund.fund_name, self.days, self.rate_value)
		

		