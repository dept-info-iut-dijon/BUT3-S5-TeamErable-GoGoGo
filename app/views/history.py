from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def history(request: HttpRequest) -> HttpResponse:
    return render(request, 'history.html')
