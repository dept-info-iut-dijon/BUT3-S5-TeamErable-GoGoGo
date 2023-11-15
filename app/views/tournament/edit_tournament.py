from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.tournament import Tournament
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
        else:
            private = bool(request.POST.get('tournament-private'))

            try:
                tournament.name = name
                tournament.description = description
                tournament.start_date = start_date
                tournament.private = private
                tournament.end_date = end_date
                tournament.organisator = organisator
                tournament.register_date = datetime.now().date()
                tournament.player_min = player_min
                tournament.save()

                ret = HttpResponse(f'/tournament?id={tournament.id}')

            except:
                ret = HttpResponseNotifError('Erreur lors de la modification du tournois.')

    elif request.method == RequestType.GET.value:
        ret = render(request, 'tournament/edit_tournament.html', {'tournament': tournament, 'checked': 'checked' if tournament.private else ''})

    return ret
