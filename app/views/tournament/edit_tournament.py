from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.tournament import Tournament
from ...models.game_configuration import GameConfiguration
from datetime import datetime
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ...utils import verify_post, verify_get

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

        try:
            name = verify_post(request, 'tournament-name', 'Le nom du tournoi est vide.')
            start_date = verify_post(request, 'start-date', 'La date de début du tournoi est vide.')
            end_date = verify_post(request, 'end-date', 'La date de fin du tournoi est vide.')
            organisator = verify_post(request, 'tournament-organizer', 'L\'organisateur du tournoi est vide.')
            description = verify_post(request, 'tournament-desc', 'La description du tournoi est vide.')
            player_min = verify_post(request, 'tournament-player-min', 'Le nombre de joueurs minimum est vide.')
            map_size = verify_post(request, 'tournament-map-size', 'Une erreur est survenue avec la taille de la carte')
            counting_method = verify_post(request, 'tournament-counting-method', 'Une erreur est survenue avec les régles')
            byo_yomi = verify_post(request, 'tournament-byo_yomi', 'Une erreur est survenue avec les paramètres')
            clock_type = verify_post(request, 'tournament-clock-type', 'Une erreur est survenue avec le temps')
            time_clock = verify_post(request, 'tournament-time-clock', 'Une erreur est survenue avec le temps')
            komi = verify_post(request, 'tournament-komi', 'Une erreur est survenue avec le komi')
            handicap = verify_post(request, 'tournament-handicap', 'Une erreur est survenue avec le handicap')
        
        except Exception as e:
            return HttpResponseNotifError(e)

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
                return HttpResponseNotifError('Erreur lors de la modification du tournois.')

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/edit_tournament.html', {'tournament': tournament, 'checked': 'checked' if tournament.private else ''})

    return ret
