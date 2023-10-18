from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

def tournament_manager(request: HttpRequest, id:int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    return render(request, 'tournament/tournament_manager.html')