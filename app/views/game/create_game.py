from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from ...models.game import Game
from datetime import datetime
import random, string, os, json
from ...logic import Board
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ..code_manager import CodeManager


def _delete_current_games(user):
    '''Fonction supprimant les parties en cours d'un utilisateur
    
    Args:
        user (CustomUser): l'utilisateur concerné
    '''
    current_games = Game.objects.filter(player1=user).filter(done=False).all()
    for game in current_games:
        if game.move_list:
            try:
                os.remove(game.move_list.path)
            except:
                pass
        game.delete()

def _create_new_game(name, description, is_private, user):
    '''Fonction permettant de creer une nouvelle partie
    
    Args:
        name (str): le nom de la partie
        description (str): la description de la partie
        is_private (bool): boolean indiquant si la partie est privee
        user (CustomUser): l'utilisateur concerné
    '''
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
        is_private = is_private,
        )
    
    file = f'dynamic/games/{game.id_game:X}.json'
    size = 6

    if not os.path.exists('dynamic/games'):
        os.makedirs('dynamic/games')
    with open(file, 'w') as f:
        b = Board(size)
        json.dump(b.export(), f)

    game.move_list = file
    game.save()

    return game


@login_required
@request_type(RequestType.GET, RequestType.POST)
def create_game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de création de partie

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de création de partie
    '''

    ret: HttpResponse = HttpResponseBadRequest()

    if request.method == RequestType.POST.value:
        name = request.POST.get('game-name')
        description = request.POST.get('game-desc', '')
        is_private = bool(request.POST.get('game-private', False))

        try:
            code_manager = CodeManager()
            code = code_manager.generate_unique_code()

            _delete_current_games(request.user)
            
            game = _create_new_game(name, description, is_private, request.user)

            ret = HttpResponseRedirect(f'/game?id={game.id_game}')

        except:
            ret = HttpResponseNotifError('Erreur lors de la création de la partie')

    elif request.method == RequestType.GET.value:
        ret = render(request, 'game/create_game.html')

    return ret
