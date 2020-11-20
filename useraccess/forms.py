from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Packages
# from django.forms import forms


class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    phonenumber = forms.CharField()

    username.widget.attrs.update(size='25')
    username.widget.attrs.update({'class': 'input100', 'placeholder':'username'})
    
    phonenumber.widget.attrs.update(size='25')
    phonenumber.widget.attrs.update({'class': 'input100', 'placeholder':'phonenumber'})

    email.widget.attrs.update(size='25')
    email.widget.attrs.update({'class': 'input100', 'placeholder':'email'})
    
    
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
