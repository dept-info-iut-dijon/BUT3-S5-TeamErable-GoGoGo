from django import forms
from django.contrib.auth.forms import forms
from ..models.custom_user import CustomUser

class ConnectForm(forms.Form):
	class Meta:
		model = CustomUser
		fields = ['username', 'password'] 

	username = forms.CharField(
        label = ('Nom d\'utilisateur')
    )

	password = forms.CharField(
		label = ('Mot de passe'),
		widget = forms.PasswordInput(attrs = {'placeholder': 'Entrez votre mot de passe'})
	)
