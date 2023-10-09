from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated: return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'register.html')
    
    if request.method == 'POST':
        # TODO: Implement registration
        return HttpResponseRedirect('/register')
