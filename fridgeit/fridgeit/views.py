from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from fridgeit.models import User
from pinterest.models.model import Pinterest
import pinterest.search as search

CLIENT_ID = "1435790"
CLIENT_SECRET = "8c8eab09fe710377c9e879872855109c9f349195"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

from django.core.urlresolvers import reverse
from fridgeit.models import User

def home(request):
	return render(request, 'landing.html')

def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def login(request):
	if request.method =="POST":
		email = request.POST.get('email')
		password = request.POST.get('password')
		username = get_user(email)		
		user = authenticate(username = username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('index')
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

def get_recipe(request):
	#Pinterest API calls (or Food 2 Fork)
	result = search.user_pin("kittens")
	return render(request, 'recipes.html')
