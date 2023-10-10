from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout



def login_(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        
    return render(request, 'login.html', {'error': 'Le mot de passe ou le nom d\'utilisateur est incorrect.'})



def logout_(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect('/login')
