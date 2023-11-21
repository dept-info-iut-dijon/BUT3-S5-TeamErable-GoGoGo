from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from datetime import datetime
from ..decorators import login_required

# Function to delete a tournament if the user is the creator
@login_required
def delete_tournament(request: HttpRequest, id_tournament: int) -> HttpResponse:
    ret = HttpResponse('Erreur lors de la suppression du tournois')
    try:
        tournament = Tournament.objects.get(id=id_tournament)
        if tournament.creator.id != request.user.id: ret = HttpResponseRedirect('/tournament')
        if tournament.start_date <= datetime.now(): ret = HttpResponseRedirect('/tournament')
        configuration = tournament.configuration
        tournament.delete()
        configuration.delete()
        ret = HttpResponseRedirect('/tournament')
    except:
        return HttpResponseRedirect('/tournament')

    return ret