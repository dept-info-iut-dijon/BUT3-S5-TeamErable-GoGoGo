from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from ..models import Game

def join_game(request: HttpRequest) -> HttpResponse:
    return render(request, 'join_game.html')

def search_game(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        query = request.POST.get('game_name','')
        games = Game.objects.filter(player2 = None).filter(done = False).exclude(player1 = request.user).filter(code = None).filter(name__icontains = query).order_by('name')[:12]
        return render(request, 'reusable/game_list.html', {'games': games})

    return HttpResponseBadRequest('')  