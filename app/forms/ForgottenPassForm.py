from django import forms

class ForgottenPassForm(forms.Form):
    '''Classe permettant de creer un formulaire lorsque le mot de passe est oublie'''
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )