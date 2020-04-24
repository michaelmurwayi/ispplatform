from django.contrib import admin
from django.urls import path, include
from .views import AdminDashboard

urlpatterns = [
    path('admin/', AdminDashboard.as_view(), name="admindashboard"),
]