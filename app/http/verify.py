from django.http import HttpRequest
from ..views.tournament.tournament_struct import TournamentStruct
from ..views.game.game_struct import GameStruct
from ..views.game.game_configuration_struct import GameConfigurationStruct

def verify_post(request: HttpRequest, key : str, message : str) -> str:
    if (value := request.POST.get(key)) is None: 
        raise Exception(message)
    return value

def verify_get(request: HttpRequest, key : str, message : str) -> str:
    if (value := request.GET.get(key)) is None: 
        raise Exception(message)
    return value

def verify_tournament(request: HttpRequest) -> TournamentStruct | Exception:
    ret = None
    try: 
        game_config = _verify_game_config(request)

        ret = TournamentStruct(
            name = verify_post(request, 'tournament-name', 'Le nom du tournoi est vide.'),
            start_date = verify_post(request, 'start-date', 'La date de début du tournoi est vide.'),
            end_date = verify_post(request, 'end-date', 'La date de fin du tournoi est vide.'),
            organisator = verify_post(request, 'tournament-organizer', 'L\'organisateur du tournoi est vide.'),
            description = verify_post(request, 'tournament-desc', 'La description du tournoi est vide.'),
            player_min = verify_post(request, 'tournament-player-min', 'Le nombre de joueurs minimum est vide.'),
            game_configuration = game_config
        )

    except Exception as e:
        ret = e

    return ret

def verify_game(request: HttpRequest) -> GameStruct | Exception:
    ret = None
    try: 
        game_config = _verify_game_config(request)

        ret = GameStruct(
            name = verify_post(request, 'game-name', 'Le nom de la partie est vide.'),
            description = verify_post(request, 'game-desc', 'La description de la partie est vide.'),
            game_configuration = game_config
        )

    except Exception as e:
        ret = e
    
    return ret

def _verify_game_config(request: HttpRequest) -> GameConfigurationStruct:
    ret = GameConfigurationStruct(
        is_private = bool(request.POST.get('game-private')),
        map_size = verify_post(request, 'map-size', 'La taille de la carte est vide.'),
        counting_method = verify_post(request, 'counting-method', 'La methode de comptage est vide.'),
        byo_yomi = verify_post(request, 'byo-yomi', 'Le byo-yomi est vide.'),
        clock_type = verify_post(request, 'clock-type', 'Le temps de la partie est vide.'),
        time_clock = verify_post(request, 'time-clock', 'Le temps de la partie est vide.'),
        komi = verify_post(request, 'komi', 'Le komi est vide.'),
        handicap = verify_post(request, 'handicap', 'Le handicap est vide.'),
        ranked = bool(request.POST.get('ranked'))
    )

    return ret