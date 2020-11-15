from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Packages
# from django.forms import forms


class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    phonenumber = forms.CharField()



    class Meta:
        model = CustomUser
        fields = [ 'username', 'email', 'phonenumber']

class TwoFactorForm(forms.ModelForm):

    class Meta:
        model=CustomUser
        fields = ['code']


class PackagesForm(forms.ModelForm):
    bundle = forms.CharField()
    bundle_price = forms.CharField()
    bundle_length = forms.CharField()
    bundle_speed = forms.CharField()

    class Meta:
        model = Packages
        fields = ['bundle', 'bundle_price', 'bundle_length', 'bundle_speed']
