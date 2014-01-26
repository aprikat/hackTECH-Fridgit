from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from fridgeit.models import User
from pinterest.models.model import Pinterest, User
from fridgeit.models import Food
from pinterest.models.model import Pinterest
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
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

def userlogin(request):
	if request.method =="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
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

def index(request):
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')

def landing(request):
	return render(request, 'landing.html')

def get_food(request):
	userId = request.GET.get('user_id')
	foods = Food.objects.filter(user=userId)
	response = serializers.serialize('json', foods, fields=('name','quantity'))
	print "Response is: " + response
	return HttpResponse(response, mimetype="application/json")

def get_recipe(request):
	if request.method == 'POST':
		print(request.params.ingredients)
	#get ingredients
	#ingredients = ['chocolate', 'strawberry', 'cream']
	ingredients = ['avocado', 'chocolate', 'lettuce']
	#ingredients = ['egg', 'pineapple', 'lettuce', 'vodka', 'dog food', 'unicorn']
	size = len(ingredients)
	pin_name = []
	pin_url = []
	pin_link = []
	pin_match = []
	
	results = search_pins(ingredients, size)
	pins_found = len(results)

	if pins_found>=25 :
		copy_results(results, pin_name, pin_url, pin_link)
		calculate_match(results, pin_match, len(ingredients), len(ingredients))
		reverse_lists(pin_name, pin_url, pin_link, pin_match)
		return render(request, 'recipes.html', {'names': pin_name, 'urls': pin_url, 'links': pin_link, 'match': pin_match, 'quartile': range(0, len(results)), 'empty': False})
	else :
		copy_results(results, pin_name, pin_url, pin_link)
		calculate_match(results, pin_match, len(ingredients), len(ingredients))
		
		results = search_pins(ingredients, size-1)
		copy_results(results, pin_name, pin_url, pin_link)
		calculate_match(results, pin_match, len(ingredients), len(ingredients)-1)
		
		pins_found = len(results)
		reverse_lists(pin_name, pin_url, pin_link, pin_match)

		if pins_found==0 :	
			return render(request, 'recipes.html', {'empty': True})
		else :
			return render(request, 'recipes.html', {'names': pin_name, 'urls': pin_url, 'links': pin_link, 'match': pin_match, 'quartile': range(0, len(results)), 'empty': False})

def search_pins(ingredients, size):
	#convert ingredients to string query
	query = ""
	for i in range(0, size):
		query = query + ingredients[i] + " "

	#prepare search results
	results = search.pins(query="fudge", rich_type="recipe", rich_query=query, restrict="food_drink", boost="quality")
	return results

def copy_results(results, pin_name, pin_url, pin_link):
	for x in range (0, len(results)):
		pin_name.append(results[x].description)
		pin_url.append(results[x].image_large_url)
		pin_link.append(results[x].link)

def calculate_match(results, pin_match, num_ing, num_search):
	percent = 1.0*num_search/num_ing*100
	percent = "{0:.2f}".format(percent)

	for x in range (0, len(results)):
		pin_match.append(percent)

	print(pin_match)

def reverse_lists(pin_name, pin_url, pin_link, pin_match):
	pin_name.reverse()
	pin_url.reverse()
	pin_link.reverse()
	pin_match.reverse()











