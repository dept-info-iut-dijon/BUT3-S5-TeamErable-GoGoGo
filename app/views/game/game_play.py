from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from app.models import Game
from ...logic import Board, Tile, RuleFactory, Vector2
import json
from ..decorators import login_required, request_type, RequestType
from ...http import HttpResponseNotifError


@login_required
@request_type(RequestType.POST)
def game_play(request: HttpRequest) -> HttpResponse:
    ret: HttpResponse = HttpResponseBadRequest()

    if (game_id := request.POST.get('id')) is None: ret = HttpResponseBadRequest()
    else:
        try:
            game_inst = Game.objects.get(id_game = game_id, done = False)
            if not game_inst: raise Exception()
            if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: raise Exception()

        except:
            return HttpResponseBadRequest()

        if game_inst.game_participate.player2 is None: ret = HttpResponseNotifError('Joueur 2 manquant.')

        elif (x := request.POST.get('x')) is None or (y := request.POST.get('y')) is None: ret = HttpResponseNotifError('Coordonnées invalides.')

        else:
            try:
                ret = HttpResponse()

                x = int(x)
                y = int(y)
                size = game_inst.game_configuration.map_size

                if x < 0 or x > size or y < 0 or y > size: ret = HttpResponseNotifError('Coordonnées invalides.')
                else:
                    board = Board(game_inst.game_configuration.map_size, RuleFactory().get(game_inst.game_configuration.counting_method))
                    with open(game_inst.move_list.path, 'r') as f:
                        board.load(json.load(f))

                    try:
                        board.play(Vector2(x, y), Tile.White if request.user == game_inst.game_participate.player1 else Tile.Black)

                        with open(game_inst.move_list.path, 'w') as f:
                            json.dump(board.export(), f)

                    except Exception as e:
                        ret = HttpResponseNotifError(str(e))

            except:
                ret = HttpResponseNotifError('Coordonnées invalides.')

    return ret


@login_required
@request_type(RequestType.POST)
def game_fetch(request: HttpRequest) -> HttpResponse:
    return HttpResponse()
