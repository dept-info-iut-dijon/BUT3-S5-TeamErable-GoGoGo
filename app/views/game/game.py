from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from app.models import Game
from ...logic import Board, Tile, RuleFactory
import json
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError

@login_required
@request_type(RequestType.GET)
def game(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de la partie

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Réponse HTTP à la requête de la partie
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if (game_id := request.GET.get('id')) is None: ret = HttpResponseRedirect('/')

    else:
        try:
            game_inst = Game.objects.get(id_game = game_id, done = False)
            if not game_inst: ret = HttpResponseRedirect('/')

        except:
            return HttpResponseRedirect('/')

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 is None and not game_inst.is_private:
            game_inst.game_participate.player2 = request.user
            game_inst.game_participate.save()

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: return HttpResponseRedirect('/')

        ret = game_logic(request, game_inst)

    return ret


@login_required
@request_type(RequestType.POST)
def game_code(request: HttpRequest) -> HttpResponse:
    '''Controlleur de la page de la partie via code

    Args:
        request (HttpRequest): La requête HTTP

    Returns:
        HttpResponse: La réponse HTTP à la requête de la partie
    '''
    ret: HttpResponse = HttpResponseBadRequest()

    if (game_code := request.POST.get('code')) is None: ret = HttpResponseNotifError('Code invalide.')

    else:
        try:
            game_inst = Game.objects.get(code = game_code, done = False)
            if not game_inst: return HttpResponseNotifError('Code invalide.')

        except:
            return HttpResponseNotifError('Code invalide.')

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 is None:
            game_inst.game_participate.player2 = request.user
            game_inst.game_participate.save()

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: return HttpResponseNotifError('Code invalide.')

        ret = HttpResponseRedirect(f'/game?id={game_inst.id_game}')

    return ret


def game_logic(request: HttpRequest, game: Game) -> HttpResponse:
    '''Logique de la page de la partie

    Args:
        request (HttpRequest): La requête HTTP
        game (Game): La partie

    Returns:
        HttpResponse: La réponse HTTP à la requête de la partie
    '''

    # TODO: LE CODE CI-DESSOUS EST TEMPORAIRE, IL FAUT LE MODIFIER DURANT LE SPRINT 3
    board = Board(game.game_configuration.map_size, RuleFactory().get(game.game_configuration.counting_method))
    with open(game.move_list.path, 'r') as f:
        board.load(json.load(f))

    return render(
        request,
        'game/game.html',
        {
            'board': board,
        }
    )
