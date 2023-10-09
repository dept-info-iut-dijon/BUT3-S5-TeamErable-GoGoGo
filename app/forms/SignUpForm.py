from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','password1', 'password2'] 

	#traduction des champs en francais
	username = forms.CharField(
        label=('Nom d\'utilisateur:')
    )

	password1 = forms.CharField(
		label=('Mot de passe:'),
		help_text=('Votre mot de passe doit contenir au moins 8 caracteres')
	)
	password2 = forms.CharField(
		label=('Confirmer le mot de passe:'),
		help_text=('Re-entrez votre mot de passe pour confirmer')
	)
	email = forms.EmailField(
		label=('Adresse Mail:'),
		help_text=('')
	)

