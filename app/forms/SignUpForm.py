from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..models.custom_user import CustomUser

class SignUpForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password1', 'password2'] 

	username = forms.CharField()
	password1 = forms.CharField()
	password2 = forms.CharField()
	email = forms.EmailField()
