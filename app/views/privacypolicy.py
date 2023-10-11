from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def privacypolicy(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'privacypolicy.html')