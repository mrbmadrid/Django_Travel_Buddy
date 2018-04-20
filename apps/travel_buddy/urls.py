from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.landing),
	url(r'^index$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^addtrip$', views.add_trip),
	url(r'^destinations/(?P<id>\d+)$', views.destination),
	url(r'^join/(?P<id>\d+)$', views.join),
	# url(r'^delete/(?P<id>\d+)$', views.delete)
]