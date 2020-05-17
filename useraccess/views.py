from django.shortcuts import render
from django.views.generic.base import TemplateView 
from django.views.generic import CreateView
from django.contrib.auth.forms import  UserChangeForm
from django.urls import reverse_lazy
from .models import Radacct, MpesaApiMpesapayment, Packages
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from .forms import UserCreationForm, PaymentForm
from django.contrib.auth.models import User
from mpesa_api.views import lipa_na_mpesa_online
 
# Create your views here.

class HomeView(TemplateView):
    # view for the default home page 

    template_name= "index.html"

class SignupView(CreateView):
    # view function for user registration 

    form_class = UserCreationForm
    success_url = reverse_lazy('profile')
    template_name = "signup.html"



class ProfileView(SingleObjectMixin, ListView):
    # view for the user profile page 

    template_name = 'profile.html'
    form_class = UserChangeForm
    user = User
    

    def get(self, request):
        # handling page get request
        account_details = Radacct.objects.filter(username='july').values('username', 'acctstarttime')  # query to access user database information
        user_data = [item for item in account_details] 
        # context = {
        #     "session_start_time": account_detail.connectinfo_start,
        #     "session_stop_time": account_detail.connectinfo_stop,
        # }
        return render(request, 'profile.html')
    

class PaymentView(CreateView):
    template_name = "payment.html"
    form_class = PaymentForm
    success_url = 'profile'
    
    def post(self, request):
        # handling payment processing form
        form = PaymentForm(request.POST)
        if form.is_valid():    
            form.save()
            lipa_na_mpesa_online(request)

        else:
            return render(request, 'profile.html')
    
class PackageView(SingleObjectMixin, ListView):
    template_name = "payment.html"
    packages = Packages
    
    def get(self, request):
        packages = [items for items in Packages.objects.all().values()]
        packages_list = []
        for items in packages:
            context = {
                "bundle": items['bundle'],
                "bundle_price": items['bundle_price'],
                "bundle_length": items['bundle_length'],
                "bundle_speed": items['bundle_speed'],
            } 
            packages_list.append(context)
        # import ipdb; ipdb.set_trace()
        return render(request, 'packages.html', {'package_list':packages_list})

def sort_user_connection_start_time(user_details):
    # get latest user connection start time 

    connectioninfo_start = user_details[-1]
    return connectioninfo_start