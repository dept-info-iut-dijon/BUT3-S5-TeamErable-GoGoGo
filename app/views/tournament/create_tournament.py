from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ...models.tournament import Tournament
from datetime import datetime
import random, string

def create_tournament(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        if (name := request.POST.get('tournament-name')) is None: return HttpResponseBadRequest('<p class="error">Le nom du tournoi est vide.</p>')
        if (start_date := request.POST.get('start-date')) is None: return HttpResponseBadRequest('<p class="error">La date de début du tournoi est vide.</p>')
        if (end_date := request.POST.get('end-date')) is None: return HttpResponseBadRequest('<p class="error">La date de fin du tournoi est vide.</p>')
        if (organisator := request.POST.get('tournament-organizer')) is None: return HttpResponseBadRequest('<p class="error">L\'organisateur du tournoi est vide.</p>')
        if (description := request.POST.get('tournament-desc', '')) is None: return HttpResponseBadRequest('<p class="error">La description du tournoi est vide.</p>')
        if (player_min := request.POST.get('tournament-player-min')) is None: return HttpResponseBadRequest('<p class="error">Le nombre de joueurs minimum est vide.</p>')
        private = bool(request.POST.get('tournament-private'))

        try:
            code = None
            while code is None or Tournament.objects.filter(code = code, end_date__gt = datetime.now()).exists():
                code = ''.join(random.choice(string.ascii_uppercase + string.octdigits) for _ in range(16))
            
            current_tournaments = Tournament.objects.filter(creator=request.user, end_date__gt = datetime.now().date()).all()

            if current_tournaments.count() > 0:
                current_tournament = current_tournaments[0]
                if datetime.now().date() >= current_tournament.start_date:
                    return HttpResponseBadRequest('<p class="error">Un tournoi en cours existe déjà. Attendez la fin de celui-ci pour en créer un nouveau.</p>')

            current_tournaments.delete()

            tournament = Tournament.objects.create(
                name = name,
                description = description,
                start_date = start_date,
                private = private,
                end_date = end_date,
                organisator = organisator,
                creator = request.user,
                register_date = datetime.now().date(),
                code = code,
                player_min = player_min
            )

            return HttpResponse(f'/tournament?id={tournament.id}')

        except:
            return HttpResponseBadRequest('<p class="error">Erreur lors de la création du tournois</p>')

    return render(request, 'create_tournament.html')
