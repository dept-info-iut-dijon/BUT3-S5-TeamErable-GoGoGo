from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from ...models.game_configuration import GameConfiguration
from datetime import datetime
import random, string
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ...utils import verify_post, verify_get


def create_tournament_post(request: HttpRequest, name: str, description: str, start_date: datetime, end_date: datetime, organisator: str, player_min: int, map_size: str, counting_method: str, byo_yomi: int, clock_type: str, time_clock: str, komi: float, handicap: int) -> HttpResponse:
    '''Créer un tournoi à partir des données du formulaire

    Args:
        request (HttpRequest): Requête HTTP
        name (str): Nom du tournoi
        description (str): Description du tournoi
        start_date (datetime): Début du tournoi
        end_date (datetime): Fin du tournoi
        organisator (str): Organisateur du tournoi
        player_min (int): Nombre de joueurs minimum

        map_size (str): Taille de la carte pour la configuration des parties
        counting_method (str): Methode de comptage pour la configuration des parties
        byo_yomi (int): Byo-yomi pour la configuration des parties
        clock_type (str): Type de horloge pour la configuration des parties
        time_clock (int): Temps de jeu pour la configuration des parties
        komi (float): Komi pour la configuration des parties
        handicap (int): Handicap pour la configuration des parties

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi créé ou erreur
    '''
    private = bool(request.POST.get('tournament-private'))

    ret: HttpResponse = HttpResponseBadRequest('Erreur lors de la création du tournois')

    try:
        code = None
        while code is None or Tournament.objects.filter(code = code, end_date__gt = datetime.now()).exists():
            code = ''.join(random.choice(string.ascii_uppercase + string.octdigits) for _ in range(16))
        
        current_tournaments = Tournament.objects.filter(creator=request.user, end_date__gt = datetime.now().date()).all()

        existing_tournament = False
        if current_tournaments.count() > 0:
            current_tournament = current_tournaments[0]
            if datetime.now().date() >= current_tournament.start_date:
                ret = HttpResponseNotifError('Un tournoi en cours existe déjà. Attendez la fin de celui-ci pour en créer un nouveau.')
                existing_tournament = True

        if existing_tournament is False:
            current_tournaments.delete()

            list_str = time_clock.split(':')
            time_clock = int(list_str[0]) * 3600 + int(list_str[1]) * 60 + int(list_str[2])

            game_configuration = GameConfiguration.objects.create(
                map_size = map_size,
                counting_method = counting_method,
                byo_yomi = byo_yomi,
                clock_type = clock_type,
                clock_value = time_clock,
                komi = komi,
                handicap = handicap,
                is_private = False
            )

            tournament = Tournament.objects.create(
                name = name,
                description = description,
                start_date = start_date,
                private = private,
                end_date = end_date,
                organisator = organisator,
                creator = request.user,
                register_date = datetime.now().date(),
                code = code,
                player_min = player_min,
                game_configuration = game_configuration
            )

            ret = HttpResponse(f'/tournament?id={tournament.id}')

    except:
        ret = HttpResponseNotifError('Erreur lors de la création du tournoi.')

    return ret

@login_required
@request_type(RequestType.GET, RequestType.POST)
def create_tournament(request: HttpRequest) -> HttpResponse:
    '''Créer un tournoi

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi créé ou erreur
    '''

    ret: HttpResponse = HttpResponseBadRequest('Erreur lors de la création du tournois')
    if request.method == RequestType.POST.value:
        
        try:
            name = verify_post(request, 'tournament-name', 'Le nom du tournoi est vide.')
            start_date = verify_post(request, 'start-date', 'La date de début du tournoi est vide.')
            end_date = verify_post(request, 'end-date', 'La date de fin du tournoi est vide.')
            organisator = verify_post(request, 'tournament-organizer', 'L\'organisateur du tournoi est vide.')
            description = verify_post(request, 'tournament-desc', 'La description du tournoi est vide.')
            player_min = verify_post(request, 'tournament-player-min', 'Le nombre de joueurs minimum est vide.')
            map_size = verify_post(request, 'tournament-map-size', 'La taille de la carte est vide.')
            counting_method = verify_post(request, 'tournament-counting-method', 'La methode de comptage est vide.')
            byo_yomi = verify_post(request, 'tournament-byo_yomi', 'Le temps de jeu est vide.')
            clock_type = verify_post(request, 'tournament-clock-type', 'Le type de horloge est vide.')
            time_clock = verify_post(request, 'tournament-time-clock', 'Le temps de jeu est vide.')
            komi = verify_post(request, 'tournament-komi', 'Le Komi est vide.')
            handicap = verify_post(request, 'tournament-handicap', 'Le Handicap est vide.')

        except Exception as e:
            return HttpResponseNotifError(str(e))

        ret = create_tournament_post(request, name, description, start_date, end_date, organisator, player_min, map_size, counting_method, byo_yomi, clock_type, time_clock, komi, handicap)

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/create_tournament.html')

    return ret
