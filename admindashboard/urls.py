from django.contrib import admin
from django.urls import path, include
from .views import AdminDashboard

urlpatterns = [
    path('admindash/', AdminDashboard.as_view(), name="admindashboard"),
]