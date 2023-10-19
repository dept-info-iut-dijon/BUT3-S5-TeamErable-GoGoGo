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
        return render(request, 'reusable/tournament_list.html', {'tournaments': tournaments})

    return HttpResponseBadRequest('')  