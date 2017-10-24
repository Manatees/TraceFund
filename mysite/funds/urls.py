from django.conf.urls import url 


from . import views

app_name = 'funds'
urlpatterns = [
	url(r'^testjson/$', views.test_json, name='test_json'),

	url(r'^$', views.HoldOnReports.as_view(), name='fund_default'),	
	url(r'^(?P<pk>[0-9]+)/$', views.TradeHistory.as_view(), name='trade_history'),
	url(r'^(?P<pk>[0-9]+)/chart/$', views.TradeChart.as_view(), name='trade_chart'),	
	url(r'^hold_on_funds/$',views.HoldOnFundsView.as_view(), name="hold_on_funds"),
	url(r'^hold_on_reports/$',views.HoldOnReports.as_view(), name="hold_on_reports"),

	url(r'^refresh_netprice/$', views.refresh_fund_netprice, name='refresh_netprice'),
	url(r'^do_confirm_shares/$',views.do_confirm_shares, name="do_confirm_shares"),
	url(r'^(?P<fund_id>[0-9]+)/purchase/$', views.purchase_fund, name="purchase"),
	url(r'^(?P<fund_id>[0-9]+)/redemption/$', views.redemption_fund, name="redemption"),
	url(r'^(?P<fund_id>[0-9]+)/liquidation/$', views.liquidation, name="liquidation"),
	url(r'^(?P<fund_code>[0-9]+)/estimated_price/$', views.estimated_price, name='estimated_price'),

	# json format
	url(r'^(?P<fund_id>[0-9]+)/chart_data/$', views.chart_data, name='chart_data'),

	url(r'^cancel_purchased/(?P<fund_id>[0-9]+)/(?P<purchase_id>[0-9]+)/$', views.cancel_purchased, name='cancel_purchased'),	
	url(r'^cancel_redemption/(?P<fund_id>[0-9]+)/(?P<redemption_id>[0-9]+)/$', views.cancel_redemption, name='cancel_redemption'),
	url(r'^purchase_detail/(?P<fund_id>[0-9]+)/(?P<purchase_id>[0-9]+)/$', views.purchase_fund_detail, name='purchase_fund_detail'),

]