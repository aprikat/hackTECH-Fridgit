from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from fridgeit.models import User

def home(request):
	return render(request, 'landing.html')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def login(request):
	print "The number of users in the table is: "
	print len(User.objects.all());
	return HttpResponseRedirect('/index.html')
	
def index(request):
	return render(request, 'index.html')
