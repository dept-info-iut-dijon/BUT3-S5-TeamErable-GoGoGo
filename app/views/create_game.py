from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ..models.partie import Partie
from datetime import datetime

def create_game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        name = request.POST.get('game-name')
        description = request.POST.get('game-desc', '')
        is_private = request.POST.get('game-private', False)

        try:
            game = Partie.objects.create(
                nom = name,
                description = description,
                dateDebut = datetime.now(),
                duree = 0,
                termine = False,
                joueur1 = request.user,
                joueur2 = None
            )
            return HttpResponse(f'/game?id={game.idPartie}')

        except:
            return HttpResponseBadRequest('<p class="error">Erreur lors de la création de la partie</p>')

    return render(request, 'create_game.html')
