from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from ..models.game import Game
from datetime import datetime
import random, string, os, json
from ..logic import Board

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
                if game.move_list:
                    try: os.remove(game.move_list.path)
                    except: pass
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
                code = code,
            )

            file = f'dynamic/games/{game.id_game:X}.json'
            size = 6

            if not os.path.exists('dynamic/games'): os.makedirs('dynamic/games')
            with open(file, 'w') as f:
                b = Board(size)
                json.dump(b.export(), f)

            game.move_list = file
            game.save()

            return HttpResponse(f'/game?id={game.id_game}')

        except:
            import traceback
            traceback.print_exc()
            return HttpResponseBadRequest('<p class="error">Erreur lors de la création de la partie</p>')

    return render(request, 'create_game.html')
