from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Packages
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from .forms import UserCreationForm, PackagesForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth import login, authenticate
import requests
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from .models import SelectedPackages
# Create your views here.


class HomeView(TemplateView):
    # view for the default home page
    template_name = "index.html"


class SignupView(CreateView):
    # view function for user registration

    form_class = UserCreationForm
    success_url = reverse_lazy('profile')
    template_name = "signup.html"

    def post(self, request):
        #  how to handle user registration form

        form = UserCreationForm(request.POST)
        if form.is_valid():
            import ipdb
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
        email = request.user.email
        user_check = SelectedPackages.objects.filter(email=email).count()
        if user_check == 0:
            context = {
                "user_count":
                user_check,
                "bundle":
                0,
                "speed":
                "0MBz",
                "Expiry":
                0,
                "Balance":
                0,
                "Connection_message":
                "Your Connection is Limited please purchase bundle"
            }
            return render(request, 'profile.html', {"context": context})
        elif user_check != 0:
            # import ipdb; ipdb.set_trace()
            user_package = UserPackage.objects.filter(email=email).last()
            expected_expiry = user_package.Expiry
            context = {
                "user_count":
                user_check,
                "bundle":
                user_package.bundle,
                "speed":
                user_package.speed,
                "Expiry":
                expected_expiry,
                "Balance":
                user_package.balance,
                "Connection_message":
                "You are connected to the internet. Enjoy browsing"
            }
            return render(request, 'profile.html', {"context": context})


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
        cache.set('email', context['email'])
        cache.set('phonenumber', "0746256084")
        # should be replaced with request.user.phonenumber
        return render(request, 'packages.html',
                      {'package_list': packages_list})


def sort_user_connection_start_time(user_details):

    # get latest user connection start time

    connectioninfo_start = user_details[-1]
    return connectioninfo_start


def get_bundle(request):
    cache.set('amount', request.GET.get('price'))
    # import ipdb; ipdb.set_trace()
    return HttpResponseRedirect(
        "http://e534efe51dd1.ngrok.io/api/v1/online/lipa")


def insert_select_package_to_db(data):
    expiry_time = calculate_expiry(data["access_period"])
    user_package = SelectedPackages(email=data["email"],
                                    bundle=data["bundle"],
                                    speed=data["speed"],
                                    Expiry=expiry_time,
                                    balance=data["bundle"],
                                    access_period=data["access_period"])
    return user_package.save()


def calculate_expiry(access_period):
    now = datetime.now()
    if access_period == 'Daily':
        expiry_time = now + timedelta(hours=24)
        return expiry_time.strftime('%Y-%m-%d-%H:%M:%S')
    elif access_period == "Weekly":
        expiry_time = now + timedelta(hours=168)
        return expiry_time.strftime('%Y-%m-%d-%H:%M:%S')
    return now
