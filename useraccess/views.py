from django.shortcuts import render, redirect 
from django.views.generic.base import TemplateView 
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import  Packages
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from .forms import UserCreationForm, PackagesForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth import login, authenticate
import requests
from django.http import HttpResponseRedirect
 
# Create your views here.

class HomeView(TemplateView):
    # view for the default home page 
    template_name= "index.html"

class SignupView(CreateView):
    # view function for user registration 

    form_class = UserCreationForm
    success_url = reverse_lazy('profile')
    template_name = "signup.html"
    
    

    def post(self, request):
        #  how to handle user registration form 

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return render(request, 'profile.html')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

class ProfileView(SingleObjectMixin, ListView):
    # view for the user profile page 

    template_name = 'profile.html'
    user = User
    

    def get(self, request):
        
        return redirect('http://55187aaf0005.ngrok.io/api/v1/online/lipa')
    

class PackageView(CreateView):
    # view class for handling internet packages 

    form_class = PackagesForm
    template_name = "packages.html"
    packages = Packages
    
    def get(self, request):
        packages = [items for items in Packages.objects.all().values()]
        packages_list = []
        form = self.form_class()
        
        for items in packages:
            context = {
                "email": request.user.email,
                "bundle": items['bundle'],
                "bundle_price": items['bundle_price'],
                "bundle_length": items['bundle_length'],
                "bundle_speed": items['bundle_speed'],
            } 
            packages_list.append(context)
        # storing user email and phonenumber in cache for later access  
        cache.set('email', context['email'] )
        cache.set('phonenumber', "0746256084" )
        # should be replaced with request.user.phonenumber
        # import ipdb; ipdb.set_trace()
        return render(request, 'packages.html', {'package_list':packages_list}) 

def sort_user_connection_start_time(user_details):
    # get latest user connection start time 

    connectioninfo_start = user_details[-1]
    return connectioninfo_start

def get_bundle(request):
    cache.set('amount', request.GET.get('price'))
    # import ipdb; ipdb.set_trace()
    return HttpResponseRedirect("http://e534efe51dd1.ngrok.io/api/v1/online/lipa")