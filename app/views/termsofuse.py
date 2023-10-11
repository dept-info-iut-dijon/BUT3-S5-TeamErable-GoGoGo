from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def termsofuse(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'termsofuse.html')