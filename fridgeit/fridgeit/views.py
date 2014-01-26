from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from fridgeit.models import User
from pinterest.models.model import Pinterest
import pinterest.search as search

CLIENT_ID = "1435790"
CLIENT_SECRET = "8c8eab09fe710377c9e879872855109c9f349195"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

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

def login(request):
	print "The number of users in the table is: "
	print len(User.objects.all());
	return HttpResponseRedirect('/index.html')
	
def index(request):
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')

def signup(request):
	return render(request, 'signup.html')

def get_recipe(request):
	#Pinterest API calls (or Food 2 Fork)
	result = search.user_pin("kittens")
	return render(request, 'recipes.html')

