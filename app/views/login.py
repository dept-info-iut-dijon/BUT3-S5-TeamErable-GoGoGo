from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from ..forms.ConnectForm import ConnectForm



def login_(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        form = ConnectForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
            if user:
                login(request, user)
                return HttpResponse()

        return HttpResponseBadRequest('<p class="error">Le mot de passe ou le nom d\'utilisateur est incorrect.</p>')
        
    return HttpResponseBadRequest()



def logout_(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect('/login')
