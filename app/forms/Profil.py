from django import forms
from django.contrib.auth.forms import forms
from ..models.person import CustomUser

class Profil(forms.Form):
	class Meta:
		model = CustomUser
		fields = ['username', 'email','password1', 'password2'] 

	#traduction des champs en francais
	username = forms.CharField(
        label=('Nom d\'utilisateur:')
    )
	email = forms.EmailField(
		label=('Adresse Mail:'),
		help_text=('')
	)
	password1 = forms.CharField(
		label=('Mot de passe:'),
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
		help_text=('Votre mot de passe doit contenir au moins 8 caracteres')
	)
	password2 = forms.CharField(
		label=('Confirmer le mot de passe:'),
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
		help_text=('Re-entrez votre mot de passe pour confirmer')
	)
	