from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ..models.partie import Partie
from datetime import datetime
import random, string

def create_game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')

    if request.method == 'POST':
        name = request.POST.get('game-name')
        description = request.POST.get('game-desc', '')
        is_private = bool(request.POST.get('game-private', False))

        try:
            code = None
            if is_private:
                while code is None or Partie.objects.filter(code = code).filter(termine = False).exists():
                    code = ''.join(random.choice(string.ascii_uppercase + string.octdigits) for _ in range(16))

            current_games = Partie.objects.filter(joueur1 = request.user).filter(termine = False).all()
            for game in current_games:
                game.delete()

            game = Partie.objects.create(
                nom = name,
                description = description,
                dateDebut = datetime.now(),
                duree = 0,
                termine = False,
                joueur1 = request.user,
                joueur2 = None,
                code = code
            )
            return HttpResponse(f'/game?id={game.idPartie}')

        except:
            return HttpResponseBadRequest('<p class="error">Erreur lors de la création de la partie</p>')

    return render(request, 'create_game.html')
