from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from ..models import Partie

def join_game(request: HttpRequest) -> HttpResponse:
    return render(request, 'join_game.html')

def search_game(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        query = request.POST.get('game_name','')
        games = Partie.objects.filter(joueur2 = None).filter(termine = False).exclude(joueur1 = request.user).filter(code = None).filter(nom__icontains = query).order_by('nom')[:12]
        return render(request, 'reusable/game_list.html', {'games': games})

    return HttpResponseBadRequest('')  