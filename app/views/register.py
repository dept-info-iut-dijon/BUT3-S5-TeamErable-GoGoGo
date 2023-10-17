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

            with open('./static/icons/default-pfp.png', 'rb') as f:
                user.profile_picture.save('default-pfp.png', f, save=True)

            return HttpResponseRedirect('/')

        else:
            password2_error = form.errors

        return render(request, 'signup.html', {'form':form, 'password2_error':password2_error})
