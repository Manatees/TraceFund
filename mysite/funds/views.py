import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Fund
from . import utilities
import time

def test_json(request):	 
	response_data = {'userName':'manatee','password':'abc123','office':'2'}
	s = json.dumps(response_data)
	d = 'jsonpcallback(%s)' % s

	return HttpResponse(d, content_type='application/json')

# def hold_on_funds(request):
# 	hold_funds = Fund.objects.all()
# 	latest_data = [fnd.latest_fund_data() for fnd in hold_funds]

'''
	刷新净值
'''
def refresh_fund_netprice(request):
	Fund.refresh_holdon_fund()
	return HttpResponseRedirect(reverse('funds:hold_on_funds'))

'''
	确认份额
'''
def do_confirm_shares(request):
	[fnd.ack_fund_shares() for fnd in Fund.objects.all()]
	return HttpResponseRedirect(reverse('funds:hold_on_reports'))

'''
	购买
'''
def purchase_fund(request, fund_id):
	fund = get_object_or_404(Fund, pk=fund_id)	
	_date = request.POST['trade_date']
	_amount = request.POST['trade_amount']
	fund.pruchasetrade_set.create(purchase_date=_date, amount=_amount)
	return HttpResponseRedirect(reverse('funds:trade_history', args=(fund.id,)))

'''
	撤消购买
'''
def cancel_purchased(rquest, fund_id, purchase_id):
	fund = get_object_or_404(Fund, pk=fund_id)
	pd = fund.pruchasetrade_set.get(pk=purchase_id)	
	pd.delete()
	return HttpResponseRedirect(reverse('funds:trade_history', args=(fund.id,)))	

def purchase_fund_detail(request, fund_id, purchase_id):
	# fund_id=15
	# purchase_id = 464
	fund = Fund.objects.get(pk=fund_id)
	purchase_detail = fund.pruchasetrade_set.get(pk=purchase_id)
	data = {'date':str(purchase_detail.purchase_date), 'amount':str(purchase_detail.amount)}
	return HttpResponse(json.dumps(data), content_type='application/json')


'''
	赎回
'''
def redemption_fund(request, fund_id):
	fund = get_object_or_404(Fund, pk=fund_id)	
	_date = request.POST['trade_date']
	_shares = request.POST['trade_amount']
	_netprice = request.POST['trade_netprice']
	_money = request.POST['trade_money']
	fund.redemptiontrade_set.create(redemption_date=_date, redemption_share_amount=_shares, net_price = _netprice, benefit_amount=_money)
	return HttpResponseRedirect(reverse('funds:trade_history', args=(fund.id,)))	

'''
	撤消赎回
'''
def cancel_redemption(rquest, fund_id, redemption_id):
	fund = get_object_or_404(Fund, pk=fund_id)
	pd = fund.redemptiontrade_set.get(pk=redemption_id)	
	pd.delete()
	return HttpResponseRedirect(reverse('funds:trade_history', args=(fund.id,)))	

'''
	清盘
'''
def liquidation(request, fund_id):
	fund = get_object_or_404(Fund, pk=fund_id)	
	[fnd.delete() for fnd in fund.pruchasetrade_set.all()]
	[fnd.delete() for fnd in fund.redemptiontrade_set.all()]
	return HttpResponseRedirect(reverse('funds:trade_history', args=(fund.id,)))		


'''
	净值估算
'''
def estimated_price(request, fund_code):
	l = time.localtime()
	t1 = (l.tm_year, l.tm_mon, l.tm_mday, 9, 30, 0, 0, 0, 0)
	s = time.mktime(t1)
	t2 = (l.tm_year, l.tm_mon, l.tm_mday, 15, 0, 0, 0, 0, 0)
	e = time.mktime(t2)
	c = time.time()

	if(c>s and c<e):
		json_data = utilities.estimated_value(fund_code)
		return HttpResponse(json.dumps(json_data), content_type='application/json')
	return HttpResponse('{}', content_type='application/json')

''' 
	净值列表
'''
class HoldOnFundsView(LoginRequiredMixin, generic.ListView):
	template_name = 'funds/hold_on_funds.html'
	context_object_name = 'hold_on_fund_list'
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get_queryset(self):
		hold_funds = Fund.objects.all()
		return [fnd.latest_fund_data() for fnd in hold_funds]

'''
	汇总
'''
class HoldOnReports(LoginRequiredMixin, generic.ListView):
	template_name = 'funds/hold_on_reports.html'
	context_object_name = 'hold_on_funds'
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

	def get_queryset(self):
		return Fund.objects.all()

'''
	交易历史
'''
class TradeHistory(LoginRequiredMixin, generic.DetailView):
	model = Fund
	template_name = 'funds/trade_history.html'
	login_url = '/login/'
	redirect_field_name = 'redirect_to'

class TradeChart(LoginRequiredMixin, generic.DetailView):
	model = Fund
	template_name = 'funds/trade_chart.html'
	login_url = '/login/'
	redirect_field_name = 'redirect_to'	

def chart_data(request, fund_id):	 
	fund = Fund.objects.get(pk=fund_id)
	netprices = fund.netprice_list()
	purchase_data = fund.trade_purchase_detail()

	data = json.dumps({'netprices': netprices, 'purchase': purchase_data})
	return HttpResponse(data, content_type='application/json')