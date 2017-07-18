from django.conf.urls import url 
from django.contrib.auth import views as auth_views

from . import views

app_name = 'login'

urlpatterns = [	
	url(r'^$', views.login_view, name='default'),
	# url(r'^$', auth_views.LoginView.as_view(),name='default'),
	# url(r'^auth/$', views.my_view, name='auth'),
	url(r'^logout/$', views.logout_view, name='logout'),
]

