from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Packages, Radcheck
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from .forms import UserCreationForm, PackagesForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth import login, authenticate
import requests
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from .models import SelectedPackages, CustomUser
import pytz
from django.http import HttpResponseRedirect
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
        username = request.user.username
        user_check = SelectedPackages.objects.filter(username=username).count()
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
            user_package = SelectedPackages.objects.filter(
                username=username).last()
            expected_expiry = user_package.Expiry
            context = {
                "user_count":
                user_check,
                "access_period":
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
                "bundle_id": items['id'],
                "username": request.user.username,
                "bundle": items['bundle'],
                "bundle_price": items['bundle_price'],
                "bundle_length": items['bundle_length'],
                "bundle_speed": items['bundle_speed'],
            }
            packages_list.append(context)

        # storing user email and phonenumber in cache for later access
        cache.set('username', context['username'])
        cache.set('phonenumber', "0746256084")
        # should be replaced with request.user.phonenumber
        return render(request, 'packages.html',
                      {'package_list': packages_list})


def check_expiry(date):
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(
        pytz.timezone("Africa/Nairobi")).strftime('%Y-%m-%d-%H:%M')
    if now > date:
        return True
    return False


def check_user_status(data):
    # check user connection status before inserting selected internet package into the database
    try:
        last_package = SelectedPackages.objects.filter(
            username=data["username"]).last()
        expiry = last_package.Expiry
        check_expiry(expiry)
        balance = last_package.balance
    except AttributeError as error:
        print("new user purchased package")
        insert_select_package_to_db(data)
        return insert_into_radcheck(data)
    else:
        last_package = SelectedPackages.objects.filter(
            username=data["username"]).last()
        expiry = last_package.Expiry
        check_expiry(expiry)
        balance = last_package.balance
        if balance != 0 or check_expiry(expiry) == False:
            print("please exhaust current package before buying new one")
            return "please exhaust current package before buying new one"
        else:
            insert_select_package_to_db(data)
            return insert_into_radcheck(data)


def insert_select_package_to_db(data):
    # insert the selected package into the db
    expiry_time = calculate_expiry(data["access_period"])
    user_package = SelectedPackages(username=data["username"],
                                    bundle=data["bundle"],
                                    speed=data["speed"],
                                    Expiry=expiry_time,
                                    balance=data["bundle"],
                                    access_period=data["access_period"])
    return user_package.save()


def insert_into_radcheck(data):
    # inserting clear text password into radcheck

    password = CustomUser.objects.filter(
        username=data["username"]).get().password
    Cleartext_Password = Radcheck(username=data["username"],
                                  attribute="Hashed_Password",
                                  op=":=",
                                  value=password)
    Cleartext_Password.save()

    # inserting access period to radcheck
    if data["access_period"] == "Hourly":
        access_period = 3600
        Access_period = Radcheck(username=data["username"],
                                 attribute="Access_period",
                                 op=":=",
                                 value=access_period)
        Access_period.save()
    elif data["access_period"] == "Daily":
        access_period = 86400
        Access_period = Radcheck(username=data["username"],
                                 attribute="Access_period",
                                 op=":=",
                                 value=access_period)
        Access_period.save()
    elif data["access_period"] == "Weekly":
        access_period = data["access_period"]
        Access_period = Radcheck(username=data["username"],
                                 attribute="Expiration",
                                 op=":=",
                                 value=calculate_expiry(access_period))
        Access_period.save()
    else:
        access_period = data["access_period"]
        Access_period = Radcheck(username=data["username"],
                                 attribute="Expiration",
                                 op=":=",
                                 value=calculate_expiry(access_period))
        Access_period.save()

    # inserting mikrotic total limit into radcheck
    mikrotic_total_limit = calculate_total_limit(data["bundle"])
    total_limit = Radcheck(username=data["username"],
                           attribute="Mikrotic-Total-Limit",
                           op=":=",
                           value=mikrotic_total_limit)
    total_limit.save()

    print("first radcheck query")


def calculate_expiry(access_period):
    #  calculate the expected expiry time of packages

    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(pytz.timezone("Africa/Nairobi"))
    if access_period == 'Hourly':
        # calculate the expected expiry for hourly packages
        expiry_time = now + timedelta(hours=1)
        return expiry_time.strftime('%Y-%m-%d-%H:%M:%S')
    elif access_period == 'Daily':
        # calculate expected expiry date for daily packages
        expiry_time = now + timedelta(hours=24)
        return expiry_time.strftime('%Y-%m-%d-%H:%M')
    elif access_period == "Weekly":
        # calculate the expected expiry for weekly packages
        expiry_time = now + timedelta(hours=168)
        return expiry_time.strftime('%Y-%m-%d-%H:%M')
    else:
        # calculate expected expiry for monthly packages
        expiry_time = now + timedelta(hours=720)
        return expiry_time.strftime('%Y-%m-%d-%H:%M')


def calculate_total_limit(bundle):
    if bundle != "UNLIMITED":
        amount = bundle[:-2]
        size = bundle[2:]
        if size == "MB":
            KB = int(1000)
            MB = int(KB**2)
            mikrotic_total_limit = int(amount) * MB
            return mikrotic_total_limit
        else:
            amount = bundle[:-2]
            size = bundle[2:]
            KB = int(1024)
            GB = int(KB**3)
            mikrotic_total_limit = int(amount) * GB
            return mikrotic_total_limit
