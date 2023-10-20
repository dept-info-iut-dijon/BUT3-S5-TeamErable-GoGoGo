from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    return render(request, 'index.html')
