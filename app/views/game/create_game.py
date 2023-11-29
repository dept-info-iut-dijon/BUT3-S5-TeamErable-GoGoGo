from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from ...models.game import Game
from ...models.game_participate import GameParticipate
from datetime import datetime
import random, string, os, json
from ...logic import Board, RuleFactory
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError
from ..code_manager import CodeManager
from ...http import verify_game
from .game_struct import GameStruct
from .game_configuration import create_game_config
from ...storage import GameStorage

def _create_new_game(request : HttpRequest, game_struct: GameStruct) -> HttpRequest:
    '''Fonction permettant de creer une nouvelle partie
    
    Args:
        request (HttpRequest): Requête HTTP
        game_srtuct (GameStruct): La nouvelle partie

    Returns:
        HttpRequest: La requête HTTP
    '''
    code = CodeManager().generate_game_code()

    configuration = create_game_config(game_struct.game_configuration)

    participate = GameParticipate.objects.create(
        player1 = request.user,
        player2 = None,
        score_player1 = 0,
        score_player2 = 0
    )
    
    game = Game.objects.create(
        name = game_struct.name,
        description = game_struct.description,
        code = code,
        start_date = datetime.now(),
        duration = 0,
        done = False,
        tournament = None,
        game_configuration = configuration,
        game_participate = participate
    )
    
    file = f'dynamic/games/{game.id_game:X}.json'

    if not os.path.exists('dynamic/games'):
        os.makedirs('dynamic/games')
    b = Board(int(game_struct.game_configuration.map_size), float(game_struct.game_configuration.komi), RuleFactory().get(game_struct.game_configuration.counting_method))
    GameStorage.save_game(file, b)

    game.move_list = file
    game.save()

    ret = HttpResponse(f'/game?id={game.id_game}')

    return ret


@login_required
@request_type(RequestType.GET, RequestType.POST)
def create_game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de création de partie

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de création de partie
    '''
    ret: HttpResponse = HttpResponseNotifError('Erreur lors de la création de la partie')

    if request.method == RequestType.POST.value:

        if (game_verif := verify_game(request)) and isinstance(game_verif, Exception):
            return HttpResponseNotifError(game_verif)

        elif _can_create_game(request) is False:
            ret = HttpResponseNotifError('Trop de parties en cours. Attendez la fin de ceux-ci pour en creer une nouvelle.')
        
        else:
            ret = _create_new_game(request, game_verif)
                

    elif request.method == RequestType.GET.value:
        ret = render(request, 'game/create_game.html')

    return ret

def _can_create_game(request : HttpRequest) -> bool:
    '''Fonction permettant de savoir si l'utilisateur peut creer une partie
    
    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        bool: True si l'utilisateur peut creer une partie, False sinon
    '''
    current_games = Game.objects.filter(game_participate__in = GameParticipate.objects.filter(player1 = request.user)).filter(done=False).all()

    can_create = False

    if current_games.count() < 5:
        can_create = True
    return can_create