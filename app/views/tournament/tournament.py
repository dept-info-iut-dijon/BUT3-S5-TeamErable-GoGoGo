from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models import Tournament
from ...models import Participate
from datetime import datetime

def tournament(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    
    return render(request, 'tournament/tournament.html')

def search_tournament(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        query = request.POST.get('tournament_name','')
        tournaments = Tournament.objects.filter(name__icontains = query).exclude(end_date__lt = datetime.now()).exclude(private = True).order_by('name')[:12]
        return render(
            request,
            'reusable/tournament_list.html',
            {'tournaments': tournaments} |
            ({'error': 'Aucune partie n\'est disponible pour le moment ou correspond à vos critères de recherche.'} if len(tournaments) == 0 else {})
        )

    return HttpResponseBadRequest('')  

def search_current_tournament(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        tournaments = (
            Tournament.objects.filter(participate = Participate.objects.filter(person_id = request.user)).filter(done = False).order_by('name')[:12]
        )[:12]
        return render(
            request,
            'reusable/tournament_list.html',
            {'tournaments': tournaments} |
            ({'error': 'Vous n\'avez aucun tournoi courant.'} if len(games) == 0 else {})
        )

    return HttpResponseBadRequest('')
