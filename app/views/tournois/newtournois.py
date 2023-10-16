from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def new_tournois(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    return render(request, 'tournois/newtournois.html')