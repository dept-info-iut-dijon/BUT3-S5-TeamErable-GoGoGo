from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models import Tournament
from ...models import ParticipateTournament
from datetime import datetime
from django.db.models import Q
from ..decorators import login_required

@login_required
def tournament(request: HttpRequest) -> HttpResponse:
    
    return render(request, 'tournament/tournament.html')

def search_tournament(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        query = request.POST.get('tournament_name','')
        tournaments = Tournament.objects.exclude(id__in = ParticipateTournament.objects.filter(person = request.user).values('tournament')).filter(name__icontains = query).exclude(end_date__lt = datetime.now()).exclude(private = True).order_by('name')[:12]
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
            Tournament.objects.filter(Q(id__in = ParticipateTournament.objects.filter(person = request.user).values('tournament')) | Q(creator = request.user)).exclude(end_date__lt = datetime.now()).order_by('name')[:12]
        )
        return render(
            request,
            'reusable/tournament_list.html',
            {'tournaments': tournaments} |
            ({'error': 'Vous n\'avez aucun tournoi courant.'} if len(tournaments) == 0 else {})
        )

    return HttpResponseBadRequest('')

@login_required
def tournament_code(request: HttpRequest) -> HttpResponse:
    ret = HttpResponseBadRequest('Erreur lors de la recherche du tournoi')
    if (tournament_code := request.POST.get('code')) is None: ret = HttpResponseBadRequest('<p class="error">Le code est vide.</p>')

    try:
        tournament_inst = Tournament.objects.get(code = tournament_code, end_date__gt = datetime.now())
        if not tournament_inst: ret = HttpResponseBadRequest('<p class="error">Code invalide.</p>')

    except:
        return HttpResponseBadRequest('<p class="error">Code invalide.</p>')

    ret = HttpResponse(f'/tournament/{tournament_inst.id}/')
    return ret
