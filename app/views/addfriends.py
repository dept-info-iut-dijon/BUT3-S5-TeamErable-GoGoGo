from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def addfriends(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'addfriends.html')