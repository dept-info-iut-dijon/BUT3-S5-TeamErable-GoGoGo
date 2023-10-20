from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from app.models import Game
from ..logic import Board, Tile
import json

def game(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    if (game_id := request.GET.get('id')) is None: return HttpResponseRedirect('/')

    try:
        game_inst = Game.objects.get(id_game = game_id, done = False)
        if not game_inst: return HttpResponseRedirect('/')

    except:
        return HttpResponseRedirect('/')

    if game_inst.player1 != request.user and game_inst.player2 is None and not game_inst.is_private:
        game_inst.player2 = request.user
        game_inst.save()

    if game_inst.player1 != request.user and game_inst.player2 != request.user: return HttpResponseRedirect('/')

    return game_logic(request, game_inst)

def game_code(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated: return HttpResponseRedirect('/login')
    if (game_code := request.POST.get('code')) is None: return HttpResponseBadRequest('<p class="error">Code invalide.</p>')

    try:
        game_inst = Game.objects.get(code = game_code, done = False)
        if not game_inst: return HttpResponseBadRequest('<p class="error">Code invalide.</p>')

    except:
        return HttpResponseBadRequest('<p class="error">Code invalide.</p>')

    if game_inst.player1 != request.user and game_inst.player2 is None:
        game_inst.player2 = request.user
        game_inst.save()

    if game_inst.player1 != request.user and game_inst.player2 != request.user: return HttpResponseBadRequest('<p class="error">Code invalide.</p>')

    return HttpResponse(f'/game?id={game_inst.id_game}')



def game_logic(request: HttpRequest, game: Game) -> HttpResponse:
    board = Board(6)
    with open(game.move_list.path, 'r') as f:
        board.load(json.load(f))

    return render(
        request,
        'game.html',
        {
            'board': board,
        }
    )
