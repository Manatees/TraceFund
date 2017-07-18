from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.urls import reverse

# Create your views here.
import logging

def login_view(request):	
	if not request.POST:
		return render(request, 'login/login.html')

	username = request.POST['username']
	password = request.POST['password']
	redirect_to = request.POST['redirect_to']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		# Redirect to a success page
		login(request, user)
		if redirect_to == '':
			return HttpResponseRedirect(reverse('funds:hold_on_reports'))
		else:
			return HttpResponseRedirect(redirect_to)
		
	else:
		# Return an 'invalid login' error message.
		context = {'result':'yes', 'err_msg':'invalid password.'}
		return render(request, 'login/login.html', context)	


# def my_view(request):
# 	username = request.POST['username']
# 	password = request.POST['password']
# 	redirect_to = request.POST['redirect_to']
# 	user = authenticate(request, username=username, password=password)
# 	if user is not None:
# 		# Redirect to a success page
# 		login(request, user)
# 		if redirect_to == '':
# 			return HttpResponseRedirect(reverse('funds:hold_on_reports'))
# 		else:
# 			return HttpResponseRedirect(redirect_to)
		
# 	else:
# 		# Return an 'invalid login' error message.
# 		context = {'result':'yes', 'err_msg':'invalid password.'}
# 		return render(request, 'login/login.html', context)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('login:default'))