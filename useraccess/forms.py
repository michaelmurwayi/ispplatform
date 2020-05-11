from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    firstname = forms.CharField()
    lastname = forms.CharField()
    phonenumber = forms.CharField()



    class Meta:
        model = User
        fields = ['firstname', 'lastname',  'email', 'phonenumber', 'password1', 'password2']
        exclude = ('username',)