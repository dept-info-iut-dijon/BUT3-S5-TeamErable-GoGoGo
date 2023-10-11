from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def aide(request: HttpRequest) -> HttpResponse:
    
    
    return render(request, 'aide.html')