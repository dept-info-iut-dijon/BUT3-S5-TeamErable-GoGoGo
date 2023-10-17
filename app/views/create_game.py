from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ..models.game import Game
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
                while code is None or Game.objects.filter(code = code).filter(done = False).exists():
                    code = ''.join(random.choice(string.ascii_uppercase + string.octdigits) for _ in range(16))

            current_games = Game.objects.filter(player1 = request.user).filter(done = False).all()
            for game in current_games:
                game.delete()

            game = Game.objects.create(
                name = name,
                description = description,
                start_date = datetime.now(),
                duration = 0,
                done = False,
                tournament = None,
                player1 = request.user,
                player2 = None,
                code = code
            )
            return HttpResponse(f'/game?id={game.idPartie}')

        except:
            return HttpResponseBadRequest('<p class="error">Erreur lors de la création de la partie</p>')

    return render(request, 'create_game.html')
