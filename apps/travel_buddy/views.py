# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bcrypt import hashpw, gensalt
from django.shortcuts import render, redirect, HttpResponse
from models import *

# Create your views here.

def landing(request):
	if 'id' in request.session:
		return redirect(index)
	return render(request, "travel_buddy/login_register.html")

def index(request):
	if not 'id' in request.session:
		return redirect(landing)
	user = User.objects.get(id=request.session['id'])
	context = {}
	context['username'] = user.name
	context['user_trips'] = user.destinations.all()
	context['other_trips'] = Destination.objects.exclude(travelers=user)
	return render(request, "travel_buddy/index.html", context)

def destination(request, id):
	if not 'id' in request.session:
		return redirect(landing)
	context = {}
	context['destination'] = Destination.objects.get(id=id)
	context['other_travelers'] = context['destination'].travelers.exclude(id=context['destination'].planned_by.id)
	return render(request, "travel_buddy/destination.html", context)

def join(request, id):
	user = User.objects.get(id=request.session['id'])
	d = Destination.objects.get(id=id)
	d.travelers.add(user)
	d.save()
	return redirect(index)

def register(request):
	register_errors={}
	if request.POST:
		if len(User.objects.filter(username=request.POST['username'])):
   			register_errors['username_duplicate'] = "This username has already been registered."
   			return render(request, "travel_buddy/login_register.html", {'register_errors' : register_errors})
   		else:
   			register_errors = User.objects.registration_validator(request.POST)
	        if len(register_errors):
	            return render(request, "travel_buddy/login_register.html", {'register_errors' : register_errors})
	        else:
	        	salt = gensalt()
	        	pw = hashpw(request.POST['password'].encode(), salt)
	        	User.objects.create(name = request.POST['name'], username = request.POST['username'], salt = salt, pw = pw)
	        	request.session['id'] = User.objects.get(username=request.POST['username']).id
	        	return redirect(index)
	return redirect(landing)

def login(request):
	login_errors={}
	if request.POST:
		if len(User.objects.filter(username=request.POST['username'])):
			user = User.objects.get(username=request.POST['username'])
			pw = user.pw
			salt = user.salt
			if hashpw(request.POST['password'].encode(), salt.encode()) == pw:
				request.session['id'] = User.objects.get(username=request.POST['username']).id
				return redirect(index)
			else:
				login_errors['exists'] = "Check your username or password."
		else:
			login_errors['exists'] = "Check your username or password."
	return render(request, "travel_buddy/login_register.html", {'login_errors':login_errors})

def add_trip(request):
	if not 'id' in request.session:
		return redirect(landing)
	if request.POST:
		print request.POST['date_depart']
		destination_errors = Destination.objects.destination_validator(request.POST)
		if len(destination_errors):
		    return render(request, "travel_buddy/add_trip.html", {'destination_errors' : destination_errors})
		else:
			user = User.objects.get(id=request.session['id'])
			d = Destination.objects.create(name = request.POST['destination'], desc = request.POST['description'], planned_by = user, date_depart = request.POST['date_depart'], date_return = request.POST['date_return'])
			d.travelers.add(user)
			d.save()
			return redirect(index)
	return render(request, "travel_buddy/add_trip.html")

def logout(request):
	request.session.clear()
	return redirect(landing)
