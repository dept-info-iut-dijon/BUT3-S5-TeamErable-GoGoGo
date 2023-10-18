from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def tournament(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    return render(request, 'tournament/tournament.html')