from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.tournament import Tournament
from ...models.game_configuration import GameConfiguration
from datetime import datetime
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError

@login_required
@request_type(RequestType.GET, RequestType.POST)
def edit_tournament(request: HttpRequest, id_tournament: int) -> HttpResponse:
    '''Controller de la page de modification d'un tournoi

    Args:
        request (HttpRequest): Requête HTTP
        id_tournament (int): Identifiant du tournoi

    Returns:
        HttpResponse: Réponse HTTP de redirection vers la page du tournoi modifié ou erreur
    '''
    ret: HttpResponse = HttpResponseNotifError('Erreur lors de la modification du tournois')
    try:
        tournament = Tournament.objects.get(id = id_tournament)

        if datetime.now().date() >= tournament.start_date:
            return HttpResponse(f'/tournament?id={tournament.id}')

    except:
        return HttpResponse('/tournament')

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
        else:
            private = bool(request.POST.get('tournament-private'))

            try:
                list_str = time_clock.split(':')
                time_clock = int(list_str[0]) * 3600 + int(list_str[1]) * 60 + int(list_str[2])

                tournament.name = name
                tournament.description = description
                tournament.start_date = start_date
                tournament.private = private
                tournament.end_date = end_date
                tournament.organisator = organisator
                tournament.register_date = datetime.now().date()
                tournament.player_min = player_min

                game_configuration = tournament.game_configuration
                game_configuration.map_size = map_size
                game_configuration.counting_method = counting_method
                game_configuration.byo_yomi = byo_yomi
                game_configuration.clock_type = clock_type
                game_configuration.time_clock = time_clock
                game_configuration.komi = komi
                game_configuration.handicap = handicap

                tournament.game_configuration = game_configuration

                tournament.save()
                game_configuration.save()

                ret = HttpResponse(f'/tournament?id={tournament.id}')

            except:
                ret = HttpResponseNotifError('Erreur lors de la modification du tournois.')

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/edit_tournament.html', {'tournament': tournament, 'checked': 'checked' if tournament.private else ''})

    return ret
