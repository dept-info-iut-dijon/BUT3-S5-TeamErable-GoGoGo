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
    total_win_tournaments = count_total_tournament(request.user, True)
    total_lose_tournaments = count_total_tournament(request.user, False)
    total_tournaments = total_win_tournaments + total_lose_tournaments
    
    total_wins = count_total_game_win(request.user)
    total_loses = count_total_game_loose(request.user)
    total_games = total_wins + total_loses
    
    total_wins_ranked = count_total_game_ranked_win(request.user)
    total_loses_ranked = count_total_game_ranked_loose(request.user)
    total_game_ranked = total_wins_ranked + total_loses_ranked

    return render(
        request, 
        'profile/career.html',
        {'total_tournaments': total_tournaments, 'total_wins_tournaments': total_win_tournaments, 'total_loses_tournaments': total_lose_tournaments,'total_games': total_games, 'total_wins': total_wins, 'total_loses': total_loses, 'total_classed_games': total_game_ranked, 'total_classed_wins': total_wins_ranked, 'total_classed_loses': total_loses_ranked}
    )

def count_total_game_ranked_win(user) -> int:
    '''Compte le nombre de parties classées gagnées ou perdu par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties classées gagnées ou perdu
    '''
    ret = CustomUser.objects.filter(id = user.id).first().stat.game_ranked_win

    return ret

def count_total_game_ranked_loose(user) -> int:
    '''Compte le nombre de parties classées gagnées ou perdu par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties classées gagnées ou perdu
    '''
    ret = CustomUser.objects.filter(id = user.id).first().stat.game_ranked_loose

    return ret

def count_total_game_win(user) -> int:
    '''Compte le nombre de parties gagnées ou perdu par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties gagnées ou perdu
    '''
    ret = CustomUser.objects.filter(id = user.id).first().stat.game_win

    return ret

def count_total_game_loose(user) -> int:
    '''Compte le nombre de parties gagnées ou perdu par un joueur

    Returns:
        int: Le nombre de parties gagnées ou perdu
    '''
    ret = CustomUser.objects.filter(id = user.id).first().stat.game_loose

    return ret

def count_total_tournament(user, result) -> int:
    '''Compte le nombre de tournois gagnés ou perdu par un joueur

    Args:
        user (CustomUser): Le joueur
        result (bool): Le résultat du tournoi recherché

    Returns:
        int: Le nombre de tournois gagnés ou perdu
    '''
    ret = 0

    tournaments = Tournament.objects.filter(id__in = ParticipateTournament.objects.filter(person = user).values('tournament').filter(win = result))

    for tournament in tournaments:
        if tournament.terminate() == True:
            ret += 1

    return ret


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

