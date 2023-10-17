from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ..models.tournament import Tournament
from datetime import datetime
import random, string

def create_tournament(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        name = request.POST.get('tournament-name')
        register_date = request.POST.get('tournament-register')
        start_date = request.POST.get('tournament-start')
        end_date = request.POST.get('tournament-end')
        organisator = request.POST.get('tournament-organisator')
        code = request.POST.get('tournament-code')
        description = request.POST.get('tournament-desc', '')

        try:
            code = None
            while code is None or Tournament.objects.filter(code = code).filter(end_date > datetime.now()).exists():
                code = ''.join(random.choice(string.ascii_uppercase + string.octdigits) for _ in range(16))

            current_tournaments = Tournament.objects.filter(creator = request.user).filter(end_date > datetime.now()).all()
            for tournament in current_tournaments:
                tournament.delete()

            tournament = Tournament.objects.create(
                name = name,
                description = description,
                start_date = start_date,
                end_date = end_date,
                organisator = organisator,
                creator = request.user,
                register_date = register_date,
                code = code
            )
            return HttpResponse(f'/tounament?id={tounament.id}')

        except:
            return HttpResponseBadRequest('<p class="error">Erreur lors de la création du tournois</p>')

    return render(request, 'create_tournament.html')
