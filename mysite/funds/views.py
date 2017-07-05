import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Fund


def test_json(request):
	response_data = {'result': 'failed', 'message': 'You messed up.'}
	return HttpResponse(json.dumps(response_data), content_type='application/json')

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
	赎回
'''
def redemption_fund(request, fund_id):
	fund = get_object_or_404(Fund, pk=fund_id)	
	_date = request.POST['trade_date']
	_amount = request.POST['trade_amount']
	fund.redemptiontrade_set.create(redemption_date=_date, redemption_share_amount=_amount)
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
	净值列表
'''
class HoldOnFundsView(generic.ListView):
	template_name = 'funds/hold_on_funds.html'
	context_object_name = 'hold_on_fund_list'

	def get_queryset(self):
		hold_funds = Fund.objects.all()
		return [fnd.latest_fund_data() for fnd in hold_funds]

'''
	汇总
'''
class HoldOnReports(generic.ListView):
	template_name = 'funds/hold_on_reports.html'
	context_object_name = 'hold_on_funds'

	def get_queryset(self):
		return Fund.objects.all()

'''
	交易历史
'''
class TradeHistory(generic.DetailView):
	model = Fund
	template_name = 'funds/trade_history.html'

