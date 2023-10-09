from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def friends(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'friends.html')