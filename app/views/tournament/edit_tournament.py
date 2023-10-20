from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from datetime import datetime
import random, string

def edit_tournament(request: HttpRequest, id_tournament: int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    try:
        tournament = Tournament.objects.get(id = id_tournament)

        if datetime.now().date() >= tournament.start_date:
            return HttpResponseRedirect(f'/tournament?id={tournament.id}')

    except:
        return HttpResponseRedirect('/tournament')

    if request.method == 'POST':
        if (name := request.POST.get('tournament-name')) is None: return HttpResponseBadRequest('<p class="error">Le nom du tournoi est vide.</p>')
        if (start_date := request.POST.get('start-date')) is None: return HttpResponseBadRequest('<p class="error">La date de début du tournoi est vide.</p>')
        if (end_date := request.POST.get('end-date')) is None: return HttpResponseBadRequest('<p class="error">La date de fin du tournoi est vide.</p>')
        if (organisator := request.POST.get('tournament-organizer')) is None: return HttpResponseBadRequest('<p class="error">L\'organisateur du tournoi est vide.</p>')
        if (description := request.POST.get('tournament-desc', '')) is None: return HttpResponseBadRequest('<p class="error">La description du tournoi est vide.</p>')
        if (player_min := request.POST.get('tournament-player-min')) is None: return HttpResponseBadRequest('<p class="error">Le nombre de joueurs minimum est vide.</p>')
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

            return HttpResponse(f'/tournament?id={tournament.id}')

        except:
            return HttpResponseBadRequest('<p class="error">Erreur lors de la modification du tournois</p>')

    return render(request, 'edit_tournament.html', {'tournament': tournament, 'checked': 'checked' if tournament.private else ''})
