from django.shortcuts import render
from django.views.generic.base import TemplateView 
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from .models import Radacct
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
# Create your views here.

class HomeView(TemplateView):
    # view for the default home page 

    template_name= "index.html"

class SignupView(CreateView):
    # view function for user registration 

    form_class = UserCreationForm
    success_url = reverse_lazy('home/')
    template_name = "signup.html"

class ProfileView(SingleObjectMixin, ListView):
    # view for the user profile page 

    template_name = 'profile.html'
    form_class = UserChangeForm

    def get(self, request):
        # handling page get request 

        account_detail = Radacct.objects.get(username= "tony") # query to access user database information
        context = {
            "username": request.user.username,
            "email": request.user.email, 
            "session_start_time": account_detail.connectinfo_start,
            "session_stop_time": account_detail.connectinfo_stop,
        }
        return render(request, 'profile.html', context)

class PaymentView(TemplateView):
    template_name = "payment.html"
    
class PackageView(TemplateView):
    template_name= "payment.html"