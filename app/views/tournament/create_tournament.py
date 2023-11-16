from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from ...models.game_configuration import GameConfiguration
from datetime import datetime
import random, string
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError


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
        import traceback
        traceback.print_exc()

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
        if (name := request.POST.get('tournament-name')) is None: ret = HttpResponseNotifError('Le nom du tournoi est vide.')
        elif (start_date := request.POST.get('start-date')) is None: ret = HttpResponseNotifError('La date de début du tournoi est vide.')
        elif (end_date := request.POST.get('end-date')) is None: ret = HttpResponseNotifError('La date de fin du tournoi est vide.')
        elif (organisator := request.POST.get('tournament-organizer')) is None: ret = HttpResponseNotifError('L\'organisateur du tournoi est vide.')
        elif (description := request.POST.get('tournament-desc', '')) is None: ret = HttpResponseNotifError('La description du tournoi est vide.')
        elif (player_min := request.POST.get('tournament-player-min')) is None: ret = HttpResponseNotifError('Le nombre de joueurs minimum est vide.')
        elif (map_size := request.POST.get('tournament-map-size')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec la taille de la carte')
        elif (counting_method := request.POST.get('tournament-counting-method')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec les règles')
        elif (byo_yomi := request.POST.get('tournament-byo_yomi')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec le byo-yomi')
        elif (clock_type := request.POST.get('tournament-clock-type')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec le type d\'horloge')
        elif (time_clock := request.POST.get('tournament-time-clock')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec le temps')
        elif (komi := request.POST.get('tournament-komi')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec le komi')
        elif (handicap := request.POST.get('tournament-handicap')) is None: ret = HttpResponseNotifError('Une erreur est survenue avec le handicap')
        

        else: ret = create_tournament_post(request, name, description, start_date, end_date, organisator, player_min, map_size, counting_method, byo_yomi, clock_type, time_clock, komi, handicap)

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/create_tournament.html')

    return ret
