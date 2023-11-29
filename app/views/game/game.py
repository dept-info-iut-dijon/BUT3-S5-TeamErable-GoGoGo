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

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 is None and not game_inst.game_configuration.is_private:
            game_inst.game_participate.player2 = request.user
            game_inst.game_participate.save()

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: return HttpResponseRedirect('/')

        ret = game_view(request, game_inst)

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

    if (game_code := request.POST.get('code')) is None: ret = HttpResponseNotifError('Le code est vide.')

    else:
        try:
            game_inst = Game.objects.get(code = game_code, done = False)
            if not game_inst: return HttpResponseNotifError('Aucune partie avec ce code.')

        except:
            return HttpResponseNotifError('Une erreur est survenue. Veuillez réessayer.')

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 is None:
            game_inst.game_participate.player2 = request.user
            game_inst.game_participate.save()

        if game_inst.game_participate.player1 != request.user and game_inst.game_participate.player2 != request.user: return HttpResponseNotifError('Vous n\'êtes pas autorisé à rejoindre la partie.')

        ret = HttpResponse(f'/game?id={game_inst.id_game}')

    return ret


def game_view(request: HttpRequest, game: Game) -> HttpResponse:
    '''Logique de la page de la partie

    Args:
        request (HttpRequest): La requête HTTP
        game (Game): La partie

    Returns:
        HttpResponse: La réponse HTTP à la requête de la partie
    '''

    board = Board(game.game_configuration.map_size,game.game_configuration.komi, RuleFactory().get(game.game_configuration.counting_method))
    with open(game.move_list.path, 'r') as f:
        board.load(json.load(f))

    tile = Tile.White if request.user == game.game_participate.player1 else Tile.Black
    can_play = board.is_player_turn(tile)

    players = [game.game_participate.player1, game.game_participate.player2]

    player1 = request.user
    player2 = players[1] if players[0] == player1 else players[0]

    player1_color = Tile.White if player1 == game.game_participate.player1 else Tile.Black
    player2_color = Tile.White if player2 == game.game_participate.player1 else Tile.Black

    player1_html = render(
        request,
        'reusable/game_player.html',
        {
            'id': 0,
            'player': player1,
            'color': player1_color.value.color,
            'other_color': player2_color.value.color,
            'score': board.get_eaten_tiles(player1_color),
        }
    ).content.decode('utf-8')
    player2_html = render(
        request,
        'reusable/game_player.html',
        {
            'id': 1,
            'player': player2,
            'color': player2_color.value.color,
            'other_color': player1_color.value.color,
            'score': board.get_eaten_tiles(player2_color),
        }
    ).content.decode('utf-8')

    return render(
        request,
        'game/game.html',
        {
            'id': game.id_game,
            'board': [
                [
                    {
                        'tile': tile if tile else '',
                        'x': x,
                        'y': y,
                    }
                    for x, tile in enumerate(row)
                ]
                for y, row in enumerate(board.raw)
            ],
            'can_play': 'can-play' * int(can_play and not board.ended),
            'player1_html': player1_html,
            'player2_html': player2_html,
            'code': game.code,
            'action_buttons_class': '' if can_play and not board.ended else 'hidden',
            # 'player_id': player_id,
        }
    )
