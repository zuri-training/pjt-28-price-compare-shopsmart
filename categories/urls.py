from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('laptop', views.laptop, name='laptop'),
    path('mobile', views.mobile, name='mobile'),
]