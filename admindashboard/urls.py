from django.contrib import admin
from django.urls import path, include
from .views import AdminDashboardView

urlpatterns = [
    path('admindash/', AdminDashboardView.as_view(), name="admindashboard"),
]