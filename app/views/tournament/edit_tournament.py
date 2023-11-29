from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.tournament import Tournament
from datetime import datetime
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from .tournament_struct import TournamentStruct


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

        if (tournament_verif := TournamentStruct.verify_tournament(request)) is Exception:
            ret = HttpResponseNotifError(tournament_verif)


        else:
            private = bool(request.POST.get('tournament-private'))

            try:
                list_str = tournament_verif.time_clock.split(':')
                tournament_verif.time_clock = int(list_str[0]) * 3600 + int(list_str[1]) * 60 + int(list_str[2])
                
                tournament.name = tournament_verif.name
                tournament.description = tournament_verif.description
                tournament.start_date = tournament_verif.start_date
                tournament.private = private
                tournament.end_date = tournament_verif.end_date
                tournament.organisator = tournament_verif.organisator
                tournament.register_date = datetime.now().date()
                tournament.player_min = tournament_verif.player_min
                
                game_configuration = tournament.game_configuration
                game_configuration.map_size = tournament_verif.map_size
                game_configuration.counting_method = tournament_verif.counting_method
                game_configuration.byo_yomi = tournament_verif.byo_yomi
                game_configuration.clock_type = tournament_verif.clock_type
                game_configuration.time_clock = tournament_verif.time_clock
                game_configuration.komi = tournament_verif.komi
                game_configuration.handicap = tournament_verif.handicap
                
                tournament.game_configuration = game_configuration
                
                tournament.save()
                game_configuration.save()

                ret = HttpResponse(f'/tournament?id={tournament.id}')

            except:
                return HttpResponseNotifError('Erreur lors de la modification du tournois.')

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/edit_tournament.html', {'tournament': tournament, 'checked': 'checked' if tournament.private else ''})

    return ret
