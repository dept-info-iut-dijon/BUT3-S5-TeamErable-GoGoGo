from django.http import HttpResponse, HttpRequest, JsonResponse
from ...decorators import login_required, request_type, RequestType
from django.shortcuts import render
from ....http import HttpResponseNotifError, HttpResponseNotifSuccess
from ....models import CustomUser, GameSave
import json

def career(request: HttpRequest) -> HttpResponse:
    '''Constructeur de la page de carriere

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
    
    total_wins_ranked = get_total_game_ranked_win(request.user)
    total_loses_ranked = get_total_game_ranked_loose(request.user)
    total_game_ranked = total_wins_ranked + total_loses_ranked

    elo = _get_elo(request.user)
    rank = _get_rank(request.user)

    return render(
        request, 
        'profile/career.html',
        {'total_tournaments': total_tournaments, 'total_wins_tournaments': total_win_tournaments, 'total_loses_tournaments': total_lose_tournaments,'total_games': total_games, 'total_wins': total_wins, 'total_loses': total_loses, 'total_classed_games': total_game_ranked, 'total_classed_wins': total_wins_ranked, 'total_classed_loses': total_loses_ranked, 'elo': elo, 'rank': rank}
    )

def get_total_game_ranked_win(user : CustomUser) -> int:
    '''Recupère le nombre de parties classées gagnées par un joueur

    Args:
        user (CustomUser): Le joueur

    Returns:
        int: Le nombre de parties classées gagnées
    '''
    return CustomUser.objects.filter(id = user.id).first().stat.game_ranked_win

def get_total_game_ranked_loose(user : CustomUser) -> int:
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

@request_type(RequestType.POST)
@login_required
def search_games_historic(request: HttpRequest) -> HttpResponse:
    '''Recherche les 5 dernières parties que le joueur à jouées

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de recherche de parties
    '''
    query = request.POST.get('game_name','')

    games = GameSave.objects.filter(user = request.user).order_by('-name')[:12]

    return render(
        request,
        'profile/games_historic.html',
        {'games': games} |
        ({'error': 'Aucune partie n\'est disponible pour le moment ou correspond à vos critères de recherche.'} if len(games) == 0 else {})
    )

def _verify_values(json_data : dict) -> bool:
    '''Verifie si les valeurs d'un fichier JSON sont valides

    Args:
        json_data (dict): Le fichier JSON

    Returns:
        bool: True si les valeurs sont valides, False sinon
    '''
    komi_values = [3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5]
    country = ['japanese', 'chinese']
    map_size = [19, 13, 9]

    rules = {
        'duration': lambda x: x >= 0,
        'map_size': lambda x: x in map_size,
        'clock_type': lambda x: x in country,
        'counting_method': lambda x: x in country,
        'handicap': lambda x: 0 <= x <= 9,
        'komi': lambda x: x in komi_values,
        'byo_yomi': lambda x: 0 <= x <= 60,
    }
    return all(rules[key](json_data[key]) for key in rules)

@request_type(RequestType.POST)
@login_required
def import_game(request : HttpRequest) -> HttpResponse:
    ''' Importe un fichier JSON
    
    Args:
        request (HttpRequest): La requête HTTP
    
    Returns:
        HttpResponse: La réponse HTTP à la requête d'importation de fichier JSON
    '''
    ret = HttpResponseNotifError('Erreur lors de l\'importation du fichier JSON')
    try:
        uploaded_file = request.FILES.get('json_file')
        json_data = json.loads(uploaded_file.file.read())
        ret = HttpResponseNotifError('Le fichier contient des valeurs invalides')

        if _verify_values(json_data) is True:
            create_game_save(request.user, json_data)
            ret = HttpResponseNotifSuccess('Fichier JSON importé')

    except Exception:
        ret = HttpResponseNotifError("Le fichier JSON est corrompu")

    return ret

def create_game_save(user, json_data) -> None:
    '''Creer une nouvelle partie sauvegarde à partir d'un fichier JSON

    Args:
        user (CustomUser): Le joueur
        json_data (dict): Le fichier JSON
    '''
    game_save = GameSave(
        user = user,
        name = json_data['name'],
        player1 = json_data['player1'],
        player2 = json_data['player2'],
        score_player1 = json_data['score_player1'],
        score_player2 = json_data['score_player2'],
        duration = json_data['duration'],
        move_list = json_data['move_list'],
        tournament = json_data['tournament'],
        map_size = json_data['map_size'],
        komi = json_data['komi'],
        counting_method = json_data['counting_method'],
        clock_type = json_data['clock_type'],
        clock_value = json_data['clock_value'],
        byo_yomi = json_data['byo_yomi'],
        handicap = json_data['handicap'],
    )
    game_save.save()

@request_type(RequestType.POST, RequestType.GET)
@login_required
def export_game(request : HttpRequest, id_game : int) -> HttpResponse:
    ''' Exporte la partie actuelle
    
    Args:
        request (HttpRequest): La requête HTTP
    
    Returns:
        HttpResponse: La réponse HTTP à la requête d'exportation de partie
    '''
    try:
        if (game := GameSave.objects.get(id_game_save = id_game)) is None:
            ret = HttpResponseNotifError('La partie n\'existe pas')

        elif request.user == game.user:
            game_data = {
                'name' : game.name,
                'player1' : game.player1,
                'player2' : game.player2,
                'score_player1' : game.score_player1,
                'score_player2' : game.score_player2,
                'duration' : game.duration,
                'move_list' : game.move_list,
                'tournament' : game.tournament,
                'map_size' : game.map_size,
                'komi' : game.komi,
                'counting_method' : game.counting_method,
                'clock_type' : game.clock_type,
                'clock_value' : game.clock_value,
                'byo_yomi' : game.byo_yomi,
                'handicap' : game.handicap
            }

            ret = JsonResponse(game_data)
            ret['Content-Disposition'] = f'attachment; filename="{game.name}.json"'

        else:
            ret = HttpResponseNotifError('Vous n\'avez pas la permission d\'exporter cette partie')

    except Exception:
        ret = HttpResponseNotifError('La partie n\'existe pas')

    return ret