# coding=utf-8

from django.db import models
from . import utilities
from decimal import Decimal
import datetime
import time

class Fund(models.Model):
	fund_name = models.CharField(max_length=200)
	fund_code = models.CharField(max_length=20)
	fund_p_rate = models.DecimalField('purchase rate', max_digits=4, decimal_places=4)
	
	def refresh_holdon_fund():
		[fnd.update() for fnd in Fund.objects.all()]

	def __str__(self):
		return '%s (%s)' % (self.fund_name, self.fund_code)

	def netprice_list(self):
		netprices = self.fundhistory_set.order_by('-date')
		return [[str(p.date), float(p.netprice)] for p in netprices]

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
	
	""" 
	!!!IMPORTANT!!!
	"""
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
		try:
			float(_note.rstrip('%'))
		except ValueError:
			_note = '0'

		self.fundhistory_set.create(date=_date, netprice=_price, note=_note)
	
	"""
		投入金额 = 赎买总金额 - 赎回总金额
	"""
	def invest_amount(self):
		return sum([fd.amount for fd in self.pruchasetrade_set.all() if fd.netprice>0]) - self.redemption_benefit_amount()
	"""
		赎回总金额
	"""
	def redemption_benefit_amount(self):
		return sum([fd.benefit_amount for fd in self.redemptiontrade_set.all() if fd.net_price>0])	

	"""
		确认买入份额 !!!IMPORTANT!!!
	"""
	def ack_fund_shares(self):
		can_update_fund = [fd for fd in self.pruchasetrade_set.all() if fd.netprice == 0]
		for f_trade in can_update_fund:
			f_trade.updateNetprice()
	'''
		确认赎回金额
	'''
	def ack_fund_amounts(self):
		pass

	"""
		持有份额 = 购买总份额 - 赎回总份额
	"""
	def hold_on_shares_count(self):
		return sum([fd.valid_shares() for fd in self.pruchasetrade_set.all()]) - self.redemption_shares_count()
	"""
		赎回总份额
	"""
	def redemption_shares_count(self):
		return sum([fd.redemption_share_amount for fd in self.redemptiontrade_set.all()])		

	"""
		持有份额明细
	"""
	def hold_on_share_details(self):
		dic = dict([(str(r_rate.rate_value), []) for r_rate in self.redemptionratetable_set.order_by('days')])
		for fd in self.pruchasetrade_set.all():
			days = fd.hold_on_days()
			shares = fd.valid_shares()
			rate = self.current_redemption_rate(days)
			dic[str(rate)].append({'id':fd.id, 'amount':shares})
		return dic

	"""
		持有金额
	"""		
	def hold_on_amount_count(self):		
		p = self.latest_fund_data().netprice
		s = self.hold_on_shares_count()
		return (p*s).quantize(Decimal('0.00')) 
	"""
		投入单价
	"""
	def hold_on_unit_price(self):		
		if self.hold_on_shares_count():
			return (self.invest_amount() / self.hold_on_shares_count()).quantize(Decimal('0.0000')) 
		return Decimal('0').quantize(Decimal('0.0000'))
	"""
		最新净值
	"""
	def latest_netprice(self):
		return self.latest_fund_data().netprice.quantize(Decimal('0.0000')) 
	"""
		最新更新时间
	"""
	def latest_date(self):
		return self.latest_fund_data().date	


	def latest_price_limit(self):
		return self.latest_fund_data().note

	"""
		持有收益
	"""
	def benefits(self):
		return (self.hold_on_amount_count()-self.invest_amount()).quantize(Decimal('0.00')) 

	"""
		持有收益率
	"""
	def benefit_rate(self):
		if self.invest_amount():
			return (self.benefits() / self.invest_amount() * 100).quantize(Decimal('0.00'))
		return Decimal('0').quantize(Decimal('0.00'))

	def trade_detail(self):
		p = [(str(pd.purchase_date), 'purchase', pd.amount, pd.netprice, pd.valid_shares()) for pd in self.pruchasetrade_set.all()]
		r = [(str(pr.redemption_date), 'redemption', pr.benefit_amount, pr.net_price, pr.redemption_share_amount) for pr in self.redemptiontrade_set.all()]
		ret = (p+r)
		ret.sort(reverse=True)
		return ret

	def trade_purchase_detail(self):
		p = [[str(pd.purchase_date), float(pd.amount), float(pd.holdon_shares)] for pd in self.pruchasetrade_set.order_by('purchase_date')]						
		return p		

	'''
		估算净值
	'''
	def estimated_price_value(self):
		data = utilities.estimated_value(self.fund_code)
		return data['gsz']	

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
	redemption_shares = models.DecimalField('redemption shares',max_digits=9, decimal_places=2, default=0)

	def __str__(self):
		return 'fund:%s date:%s amount:%g' % (self.fund, self.purchase_date, self.amount)

	'''
		净购买金额	
	'''
	def net_purchase_amount(self):
		return (self.amount / (1 + self.fund.fund_p_rate))

	'''
		有效份额 = holdon_shares - redemptio_shares
	'''
	def valid_shares(self):
		return self.holdon_shares - self.redemption_shares

	def update_redemption_shares(self, shares_count):
		rest_count = shares_count - self.holdon_shares
		if rest_count >= 0:
			self.redemptio_shares = self.holdon_shares
			return rest_count
		else:
			self.redemptio_shares = abs(rest_count)
			return 0


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
	'''
		持有天数
	'''
	def hold_on_days(self):
		current_date = datetime.datetime.now().date()
		baseline_date = self.purchase_date
		return (current_date - baseline_date).days				


class RedemptionTrade(models.Model):
	fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
	redemption_date = models.DateField()
	redemption_share_amount = models.DecimalField(max_digits=9, decimal_places=2)
	redemption_fee = models.DecimalField(max_digits=9, decimal_places=2, default=0)
	net_price = models.DecimalField(max_digits=6, decimal_places=4, default=0)
	benefit_amount = models.DecimalField('benefit amount', max_digits=9, decimal_places=2, default=0)

