from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from ..forms.ConnectForm import ConnectForm



def login_(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        form = ConnectForm()
        return render(request, 'login.html', {'form': form})
    
    if request.method == 'POST':
        form = ConnectForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        
    return render(request, 'login.html', {'error': 'Le mot de passe ou le nom d\'utilisateur est incorrect.', 'form': ConnectForm()})



def logout_(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect('/login')
