from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def delfriends(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'delfriends.html')