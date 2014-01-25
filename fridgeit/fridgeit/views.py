from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect

def home(request):
	return render(request, 'index.html')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')



