from django.conf.urls import url 

from . import views

app_name = 'funds'
urlpatterns = [
	url(r'^testjson/$', views.test_json, name='test_json'),
	url(r'^hold_on_funds/$',views.HoldOnFundsView.as_view(), name="hold_on_funds"),
	url(r'^refresh_netprice/$', views.refresh_fund_netprice, name='refresh_netprice'),
]