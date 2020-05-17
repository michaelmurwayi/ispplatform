from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User
from .models import MpesaApiMpesapayment

class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    firstname = forms.CharField()
    lastname = forms.CharField()
    phonenumber = forms.CharField()



    class Meta:
        model = User
        fields = ['firstname', 'lastname',  'email', 'phonenumber', 'password1', 'password2']
        exclude = ('username',)

class PaymentForm(forms.ModelForm):
    phonenumber = forms.CharField()
    amount = forms.IntegerField()

    class Meta:
        model = MpesaApiMpesapayment
        fields = ['phonenumber', 'amount']