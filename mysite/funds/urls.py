from django.conf.urls import url 

from . import views

app_name = 'funds'
urlpatterns = [
	url(r'^testjson/$', views.test_json, name='test_json'),

	url(r'^$', views.HoldOnReports.as_view(), name="index"),
	url(r'^(?P<pk>[0-9]+)/$', views.TradeHistory.as_view(), name='trade_history'),
	url(r'^hold_on_funds/$',views.HoldOnFundsView.as_view(), name="hold_on_funds"),
	url(r'^hold_on_reports/$',views.HoldOnReports.as_view(), name="hold_on_reports"),

	url(r'^refresh_netprice/$', views.refresh_fund_netprice, name='refresh_netprice'),
	url(r'^do_confirm_shares/$',views.do_confirm_shares, name="do_confirm_shares"),
]