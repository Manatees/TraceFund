# coding=utf-8

from django.db import models
from . import utilities
import datetime

class Fund(models.Model):
	fund_name = models.CharField(max_length=200)
	fund_code = models.CharField(max_length=20)
	fund_p_rate = models.DecimalField('purchase rate', max_digits=4, decimal_places=4)
	
	def refresh_holdon_fund():
		[fnd.update() for fnd in Fund.objects.all()]

	def __str__(self):
		return '%s (%s)' % (self.fund_name, self.fund_code)

	def latest_fund_data(self):		
		fh = self.fundhistory_set.order_by('-date')
		if len(fh) > 0:
			return fh[0]

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
		update_records = 100
		if self.latest_fund_data() == None:
			self.__update_forced(update_records)
		else:
			self.__udpate_smarted()
	
	def __update_forced(self, days):
		r_data = self.__refresh_fund_data(days)
		[self.__insert_history(fnd[0], fnd[1], fnd[3]) for fnd in r_data]

	def __udpate_smarted(self):
		current_date = datetime.datetime.now().date()
		baseline_date = self.latest_fund_data().date
		diff_days = (current_date - baseline_date).days
		r_data = self.__refresh_fund_data(diff_days)
		[self.__insert_history(fnd[0], fnd[1], fnd[3]) for fnd in r_data if fnd[0] > str(baseline_date)]		

	def __insert_history(self, _date, _price, _note):		
		self.fundhistory_set.create(date=_date, netprice=_price, note=_note)

class FundHistory(models.Model):
	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	date = models.DateField('history date')
	netprice = models.DecimalField('net price', max_digits=6, decimal_places=4)
	note = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return '%s -> %g, %s' % (self.fund.fund_name, self.netprice, self.date)

class RedemptionRateTable(models.Model):
	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	days = models.IntegerField('in thers days', default=0)
	rate_value = models.DecimalField(max_digits=4, decimal_places=4, default=0)

	def __str__(self):
		return '%s -> %d: %g' % ( self.fund.fund_name, self.days, self.rate_value)
		

class PruchaseTrade(models.Model):
	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	purchase_date = models.DateField()
	amount = models.DecimalField(max_digits=9, decimal_places=2)
	ack_amount = models.DecimalField('net amount', max_digits=9, decimal_places=2, default=0)
	netprice = models.DecimalField(max_digits=6, decimal_places=4, default=0)
	holdon_shares = models.DecimalField('hold on shares',max_digits=9, decimal_places=2, default=0)

	def __str__(self):
		return 'fund:%s date:%s amount:%g' % (self.fund, self.purchase_date, self.amount)

	def net_purchase_amount(self):
		return (self.amount / (1 + self.fund.fund_p_rate))

	def calc_holdon_shares(self):	
		if self.netprice>0.0 :
			return (self.net_purchase_amount() / self.netprice)

	def updateNetprice(self):
		fhs = self.fund.fundhistory_set.filter(date = self.purchase_date)		
		if len(fhs) > 0:
			fh = fhs[0]
			self.netprice  =fh.netprice
			self.ack_amount = self.net_purchase_amount()
			self.holdon_shares = self.calc_holdon_shares()
			self.save()

	def hold_on_days(self):
		current_date = datetime.datetime.now().date()
		baseline_date = self.purchase_date
		return (current_date - baseline_date).days				


