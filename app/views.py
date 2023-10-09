from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")

def register(request: HttpRequest) -> HttpResponse:
    return render(request, "register.html")
