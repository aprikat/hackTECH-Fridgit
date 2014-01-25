from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect

def home(request):
	return render(request, 'landing.html')
def login(request):
	if request.method =="POST":
		email = request.POST['email']
		password = request.POST['password']
		print email, password
	return HttpResponseRedirect('/')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
	
def index(request):
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')
