from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from ..models import Game

def join_game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    return render(request, 'join_game.html')

def search_game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        query = request.POST.get('game_name','')
        games = Game.objects.filter(player2 = None).filter(done = False).exclude(player1 = request.user).filter(is_private = False).filter(name__icontains = query).order_by('name')[:12]
        return render(
            request,
            'reusable/game_list.html',
            {'games': games} |
            ({'error': 'Aucune partie n\'est disponible pour le moment ou correspond à vos critères de recherche.'} if len(games) == 0 else {})
        )

    return HttpResponseBadRequest('')

def search_current_game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        games = (
            Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user)).filter(done = False).order_by('name')[:12]
        )[:12]
        return render(
            request,
            'reusable/game_list.html',
            {'games': games} |
            ({'error': 'Vous n\'avez aucune partie courante.'} if len(games) == 0 else {})
        )

    return HttpResponseBadRequest('')
