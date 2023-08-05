"""
from django.conf.urls import url
from ApiApp import views

urlpatterns=[
    url(r'^peticion$', views.peticionApi),
    url(r'^peticion/([0-9]+)$', views.peticionApi)
]
"""


from django.urls import path
from ApiApp import views

urlpatterns = [
    path('peticionApi/', views.peticionApi),
    path('peticionApi/<id>', views.peticionApi),
]