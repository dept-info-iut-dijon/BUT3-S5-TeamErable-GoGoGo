from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from ..forms.SignUpForm import SignUpForm

def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        form = SignUpForm(request.POST)
        return render(request, 'signup.html', {'form':form})
    
    password2_error = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')

        else:
            # Check if the "Password2 didn't match" error occurred
            if 'password2' in form.errors:
                password2_error = "Vos mots de passe ne correspondent pas ou ne sont pas corrects."

        return render(request, 'signup.html', {'form':form, 'password2_error':password2_error})
