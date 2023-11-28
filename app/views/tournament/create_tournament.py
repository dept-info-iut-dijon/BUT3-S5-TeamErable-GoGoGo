from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from ...models.game_configuration import GameConfiguration
from datetime import datetime
import random, string
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ...http import verify_tournament
from .tournament_struct import TournamentStruct

def can_create_tournament(request: HttpRequest) -> bool :
    '''Fonction permettant de savoir si il est possible de creer un tournoi

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        bool: True si il est possible de creer un tournoi, False sinon
    '''
    current_tournaments = Tournament.objects.filter(creator=request.user, end_date__gt = datetime.now().date()).all()

    can_create = True
    if current_tournaments.count() > 2:
        can_create = False

    return can_create

def generation_code() -> str:
    '''Fonction permettant de generer un code de 16 caractères

    Returns:
        str: Le code de 16 caractères
    '''
    code = None
    while code is None or Tournament.objects.filter(code = code, end_date__gt = datetime.now()).exists():
        code = ''.join(random.choice(string.ascii_uppercase + string.octdigits) for _ in range(16))
    return code

def create_tournament_post(request: HttpRequest, tournament_struct: TournamentStruct) -> HttpResponse:
    '''Créer un tournoi à partir des données du formulaire

    Args:
        request (HttpRequest): Requête HTTP
        tournament_struct (TournamentStruct): Le tournoi a créer

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi créé ou erreur
    '''
    private = bool(request.POST.get('tournament-private'))

    ret: HttpResponse = HttpResponseBadRequest('Erreur lors de la création du tournois')

    try:
        code = generation_code()

        if can_create_tournament(request) is False:
            ret = HttpResponseNotifError('Trop de tournois en cours. Attendez la fin de ceux-ci pour en creer un nouveau ou supprimez en un.')

        else:
            list_str = tournament_struct.time_clock.split(':')
            tournament_struct.time_clock = int(list_str[0]) * 3600 + int(list_str[1]) * 60 + int(list_str[2])

            game_configuration = GameConfiguration.objects.create(
                map_size = tournament_struct.map_size,
                counting_method = tournament_struct.counting_method,
                byo_yomi = tournament_struct.byo_yomi,
                clock_type = tournament_struct.clock_type,
                clock_value = tournament_struct.time_clock,
                komi = tournament_struct.komi,
                handicap = tournament_struct.handicap,
                is_private = False
            )

            tournament = Tournament.objects.create(
                name = tournament_struct.name,
                description = tournament_struct.description,
                start_date = tournament_struct.start_date,
                private = private,
                end_date = tournament_struct.end_date,
                organisator = tournament_struct.organisator,
                creator = request.user,
                register_date = datetime.now().date(),
                code = code,
                player_min = tournament_struct.player_min,
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
        
        if (tournament_verif := verify_tournament(request)) is Exception:
            return HttpResponseNotifError(tournament_verif)

        ret = create_tournament_post(request, tournament_verif)

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/create_tournament.html')

    return ret
