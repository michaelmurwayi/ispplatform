from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class AdminDashboard(TemplateView):
    template_name = "admindash.html"