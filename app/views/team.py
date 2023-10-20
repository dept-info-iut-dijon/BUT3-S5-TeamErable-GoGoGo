from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def team(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'team.html')