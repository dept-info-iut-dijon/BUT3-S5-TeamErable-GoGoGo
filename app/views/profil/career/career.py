from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...decorators import login_required, request_type, RequestType
from django.shortcuts import render
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess
from ....models import Game, ParticipateTournament, CustomUser, Tournament

def career(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de carriere

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: La page de carriere
    '''
    total_wins = _get_total_game_win(request.user)
    total_loses = _get_total_game_loose(request.user)
    total_games = total_wins + total_loses

    total_win_tournaments = _get_total_tournament_win(request.user)
    total_lose_tournaments = _get_total_tournament_loose(request.user)
    total_tournaments = total_win_tournaments + total_lose_tournaments
    
    total_wins_ranked = _get_total_game_ranked_win(request.user)
    total_loses_ranked = _get_total_game_ranked_loose(request.user)
    total_game_ranked = total_wins_ranked + total_loses_ranked

    elo = _get_elo(request.user)
    rank = _get_rank(request.user)

    return render(
        request, 
        'profile/career.html',
        {'total_tournaments': total_tournaments, 'total_wins_tournaments': total_win_tournaments, 'total_loses_tournaments': total_lose_tournaments,'total_games': total_games, 'total_wins': total_wins, 'total_loses': total_loses, 'total_classed_games': total_game_ranked, 'total_classed_wins': total_wins_ranked, 'total_classed_loses': total_loses_ranked, 'elo': elo, 'rank': rank}
    )

def _get_total_game_ranked_win(user : CustomUser) -> int:
    '''Recupère le nombre de parties classées gagnées par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties classées gagnées
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.game_ranked_win

def _get_total_game_ranked_loose(user : CustomUser) -> int:
    '''Recupère le nombre de parties classées perdu par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties classées perdu
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.game_ranked_loose

def _get_total_game_win(user : CustomUser) -> int:
    '''Recupère le nombre de parties gagnées par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties gagnées
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.game_win

def _get_total_game_loose(user : CustomUser) -> int:
    '''Recupère le nombre de parties perdu par un joueur

    Returns:
        int: Le nombre de parties perdu
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.game_loose

def _get_total_tournament_win(user : CustomUser) -> int:
    '''Recupère le nombre de tournois gagnés par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de tournois gagnés
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.tournament_win

def _get_total_tournament_loose(user : CustomUser) -> int:
    '''Recupère le nombre de tournois perdu par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de tournois perdu
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.tournament_loose

def _get_elo(user : CustomUser) -> int:
    '''Recupère l'elo du joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: L'elo du joueur
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.elo

def _get_rank(user : CustomUser) -> str:
    '''Recupère le rang du joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        str: Le rang du joueur
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.rank


def search_games_historic(request: HttpRequest) -> HttpResponse:
    '''Recherche les parties que le joueur à jouées et sauvegardées

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de recherche de parties
    '''
    query = request.POST.get('game_name','')
    games = Game.objects.filter(done = True)[:12]
    return render(
        request,
        'profile/games_historic.html',
        {'games': games} |
        ({'error': 'Aucune partie n\'est disponible pour le moment ou correspond à vos critères de recherche.'} if len(games) == 0 else {})
    )

