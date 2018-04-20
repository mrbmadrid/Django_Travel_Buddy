# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
import re
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
		errors = {}
		if not re.match(r'^[a-zA-Z ]*$', postData['name']):
			errors['name'] = "Name must only be upper or lower case letters and spaces."
		if not re.match(r"^[a-zA-Z0-9_]*$", postData['username']):
			errors['username'] = "Username must be alphanumeric."
		if len(postData['name']) < 3:
			errors['name_length'] = "Name must be at least 3 characters."
		if len(postData['username']) < 3:
			errors['username_length'] = "Username must be at least 3 characters."	
		if not postData['password'] == postData['confirm']:
			errors['password_mismatch'] = "Passwords do not match."
		if len(postData['password']) < 8:
			errors['password_length'] = "Password must be greater than 8 characters in length."
		if len(postData['password']) > 16:
			errors['password_length'] = "Password must be no more than 16 characters in length."
		return errors

class DestinationManager(models.Manager):
	def destination_validator(self, postData):
		errors = {}
		if not re.match(r'^[a-zA-Z ]*$', postData['destination']):
			errors['name'] = "Destination must only be upper or lower case letters and spaces."
		if datetime.strptime(postData['date_depart'], '%Y-%m-%d') > datetime.strptime(postData['date_return'], '%Y-%m-%d'):
			errors['order'] = "Your return date must be after your departure date."
		if datetime.strptime(postData['date_depart'], '%Y-%m-%d') < datetime.now():
			errors['past'] = "Your departure date is in the past."
		return errors

class User(models.Model):
	name = models.CharField(max_length=50)
	username = models.CharField(max_length = 255, unique=True)
	salt = models.CharField(max_length=255)
	pw = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = UserManager()

class Destination(models.Model):
	name = models.CharField(max_length=255)
	planned_by = models.ForeignKey(User, related_name="trips_planned")
	desc = models.TextField(default="No description provided.")
	travelers = models.ManyToManyField(User, related_name="destinations")
	created_at = models.DateTimeField(auto_now_add=True)
	date_depart = models.DateField()
	date_return = models.DateField()
	objects = DestinationManager()
