from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect

def home(request):
	return render(request, 'landing.html')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
	
def index(request):
	return render(request, 'index.html')
