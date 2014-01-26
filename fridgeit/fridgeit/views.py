from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from fridgeit.models import User
from pinterest.models.model import Pinterest, User
from fridgeit.models import Food
#from fridgeit.models import User
from django.contrib.auth.models import User
from pinterest.models.model import Pinterest
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.hashers import make_password
import pinterest.search as search

CLIENT_ID = "1435790"
CLIENT_SECRET = "8c8eab09fe710377c9e879872855109c9f349195"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
def home(request):
	return render(request, 'landing.html')


def userlogin(request):
	if request.method =="POST":
		print request.POST
		username = request.POST.get('username')
		password = request.POST.get('password')
#		username = get_user(email)		
		print username
		user = authenticate(username = username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				print "logged {} in ".format(user.username)
				return HttpResponseRedirect('/index')
	return HttpResponseRedirect('/')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def signup(request):
	return render(request, 'signup.html')

def get_food(request):
        print "Here"
	#user = User.objects.filter(username=request.user)
	userId = 1
	foods = Food.objects.filter(user=userId)
	response = serializers.serialize('json', foods, fields=('name','quantity'))
	print "Response is: " + response
	return HttpResponse(response, mimetype="application/json")

def index(request):
	if request.user:
		food = get_food(request)
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')

def validate(request):
	if request.method =="POST":
		print(request.POST)
		username = request.POST.get('username')
		fullname = request.POST.get('name')
		password = request.POST.get('password')
		email = request.POST.get('email')
		print username, fullname, email
		fname,lname = fullname.split(" ")
		newuser= User()
		newuser.first_name = fname
		newuser.last_name = lname
		newuser.email = email
		newuser.username = username
		newuser.password = make_password(password)
		newuser.save()
		print newuser.last_name, newuser.username, newuser.email,newuser.first_name 
		print "Registered {}".format(newuser.username)
		return HttpResponseRedirect('/index')
	return HttpResponseRedirect('/')

def delete_food(request):
	foodId = request.POST.get('food_id')
	food = Food.objects.get(id = foodId)
	food.delete()
        return HttpResponse(response, mimetype="application/json")

def add_food(request):
	name = request.POST.get('food_name')
	quantity = request.POST.get('quantity')
        if name == None :
	  return HttpResponse(response, mimetype="application/json")
	userId = 1
        #userId = request.POST.get('user_id')
	u = User.objects.get(id = userId)
	f = Food(name = name, quantity = quantity, user = u)
	f.save()
        return HttpResponse(response, mimetype="application/json")

def get_recipe(request):
	#print request.POST
    ingredients = request.POST.get("ingreds")
    print ingredients

    results = search.pins(query="chicken", rich_type="recipe", rich_query=ingredients, restrict="food_drink", boost="quality")
    pins_found = len(results)
    pin_name = []
    pin_url = []
    pin_link = []

    for x in range (0, pins_found):
        pin_name.append(results[x].description)
        pin_url.append(results[x].image_large_url)
        pin_link.append(results[x].link)

    reverse_lists(pin_name, pin_url, pin_link)

    if pins_found == 0 :
    	return render(request, 'recipes.html', {'empty': True})
    else :
    	return render(request, 'recipes.html', {'names': pin_name, 'urls': pin_url, 'links': pin_link, 'quartile': range(0, pins_found)})

def reverse_lists(pin_name, pin_url, pin_link):
	pin_name.reverse()
	pin_url.reverse()
	pin_link.reverse()
