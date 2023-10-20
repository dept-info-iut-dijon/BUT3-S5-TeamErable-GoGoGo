from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from datetime import datetime


# Function to delete a tournament if the user is the creator
def delete_tournament(request: HttpRequest, id_tournament: int) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    try:
        tournament = Tournament.objects.get(id=id_tournament)
        if tournament.creator.id != request.user.id: return HttpResponseRedirect('/tournament')
        if tournament.start_date <= datetime.now(): return HttpResponseRedirect('/tournament')
        tournament.delete()
        return HttpResponseRedirect('/tournament')
    except:
        return HttpResponseRedirect('/tournament')