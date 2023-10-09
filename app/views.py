from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')

def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        print(f'connect: {request.POST}')
        return HttpResponseRedirect('/login')

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'register.html')
    
    if request.method == 'POST':
        print(f'register: {request.POST}')
        return HttpResponseRedirect('/register')
