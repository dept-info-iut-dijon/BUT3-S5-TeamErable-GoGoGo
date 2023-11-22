from django.http import HttpRequest
from ..views.tournament.tournament_struct import TournamentStruct

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
        ret = TournamentStruct(
        name = verify_post(request, 'tournament-name', 'Le nom du tournoi est vide.'),
        start_date = verify_post(request, 'start-date', 'La date de début du tournoi est vide.'),
        end_date = verify_post(request, 'end-date', 'La date de fin du tournoi est vide.'),
        organisator = verify_post(request, 'tournament-organizer', 'L\'organisateur du tournoi est vide.'),
        description = verify_post(request, 'tournament-desc', 'La description du tournoi est vide.'),
        player_min = verify_post(request, 'tournament-player-min', 'Le nombre de joueurs minimum est vide.'),
        map_size = verify_post(request, 'tournament-map-size', 'Une erreur est survenue avec la taille de la carte'),
        counting_method = verify_post(request, 'tournament-counting-method', 'Une erreur est survenue avec les régles'),
        byo_yomi = verify_post(request, 'tournament-byo_yomi', 'Une erreur est survenue avec les paramètres'),
        clock_type = verify_post(request, 'tournament-clock-type', 'Une erreur est survenue avec le temps'),
        time_clock = verify_post(request, 'tournament-time-clock', 'Une erreur est survenue avec le temps'),
        komi = verify_post(request, 'tournament-komi', 'Une erreur est survenue avec le komi'),
        handicap = verify_post(request, 'tournament-handicap', 'Une erreur est survenue avec le handicap')
        )

    except Exception as e:
        ret = e
    
    return ret