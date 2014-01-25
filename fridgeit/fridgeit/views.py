from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect

def home(request):
<<<<<<< HEAD
	return render(request, 'index.html')

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')



=======
	return render(request, 'landing.html')

def index(request):
	return render(request, 'index.html')
>>>>>>> 421aede0d9e2935db95b366182de2b9690b0b7a0
