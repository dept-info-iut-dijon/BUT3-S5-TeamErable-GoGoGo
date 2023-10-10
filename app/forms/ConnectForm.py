from django import forms
from django.contrib.auth.forms import UserChangeForm
from ..models_dir.person import CustomUser

class ConnectForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password'] 

	username = forms.CharField(
        label = ('Nom d\'utilisateur:')
    )

	password = forms.CharField(
		label = ('Mot de passe:'),
		widget = forms.PasswordInput(attrs = {'placeholder': 'Entrez votre mot de passe'})
	)
