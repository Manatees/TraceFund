from django.db import models
from . import utilities
import datetime

class Fund(models.Model):
	fund_name = models.CharField(max_length=200)
	fund_code = models.CharField(max_length=20)
	fund_p_rate = models.DecimalField('purchase rate', max_digits=4, decimal_places=4)
	

	def __str__(self):
		return '%s (%s)' % (self.fund_name, self.fund_code)

	def latest_fund_data(self):		
		return self.fundhistory_set.order_by('-date')[0]

	def current_redemption_rate(self, current_days):
		rates = list(self.redemptionratetable_set.order_by('days'))
		return Fund.__get_valid_redemption_rate(rates, current_days)
	
	def __get_valid_redemption_rate(rates, days):
		for rate in rates[:-1]:
			if days < rate.days:
				return rate.rate_value
		return rates[-1].rate_value


	def __refresh_fund_data(self, in_days):
		return utilities.do_it(self.fund_code, in_days)

	def update(self):
		current_date = datetime.datetime.now().date()
		diff_days = (current_date - self.latest_fund_data().date).days
		self.latest_remote_fund_data = self.__refresh_fund_data(diff_days)


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
		

		