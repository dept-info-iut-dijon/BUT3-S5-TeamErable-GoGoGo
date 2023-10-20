from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def help(request: HttpRequest) -> HttpResponse:
    return render(request, 'help.html')
