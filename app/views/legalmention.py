from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def legalmention(request: HttpRequest) -> HttpResponse:
    
    
    return render(request, 'legalmention.html')