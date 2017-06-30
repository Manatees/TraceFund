import json
from django.shortcuts import render
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

def refresh_fund_netprice(request):
	Fund.refresh_holdon_fund()
	return HttpResponseRedirect(reverse('funds:hold_on_funds'))

class HoldOnFundsView(generic.ListView):
	template_name = 'funds/hold_on_funds.html'
	context_object_name = 'hold_on_fund_list'

	def get_queryset(self):
		hold_funds = Fund.objects.all()
		return [fnd.latest_fund_data() for fnd in hold_funds]