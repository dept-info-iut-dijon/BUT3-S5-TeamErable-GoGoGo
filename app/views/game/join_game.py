from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from ...models import Game
from ...models.game_configuration import GameConfiguration
from ...models.game_participate import GameParticipate
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError, HttpResponseNotifSuccess

@login_required
@request_type(RequestType.GET)
def join_game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de recherche de parties

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de recherche de parties
    '''
    return render(request, 'game/join_game.html')


@login_required
@request_type(RequestType.POST)
def search_game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la requête de recherche de parties

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de recherche de parties
    '''
    query = request.POST.get('game_name','')
    games = Game.objects.filter(game_participate__in = GameParticipate.objects.filter(player2 = None)).filter(done = False).exclude(game_participate__in = GameParticipate.objects.filter(player1 = request.user)).filter(game_configuration__in = GameConfiguration.objects.filter(is_private = False)).filter(name__icontains = query).order_by('name')[:12]
    return render(
        request,
        'reusable/game_list.html',
        {'games': games} |
        ({'error': 'Aucune partie n\'est disponible pour le moment ou correspond à vos critères de recherche.'} if len(games) == 0 else {})
    )


@login_required
@request_type(RequestType.POST)
def search_current_game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la requête de recherche de parties courantes

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de recherche de parties courantes
    '''
    games = (
        Game.objects.filter(Q(game_participate__in = GameParticipate.objects.filter(player1 = request.user)) | Q(game_participate__in = GameParticipate.objects.filter(player2 = request.user))).filter(done = False).order_by('name')[:12]
        
        )[:12]
    return render(
        request,
        'reusable/game_list.html',
        {'games': games} |
        ({'error': 'Vous n\'avez aucune partie courante.'} if len(games) == 0 else {})
    )
