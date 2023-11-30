from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ..game.create_game import construct_game, construct_participate
from ...models.custom_user import CustomUser
from ..game.game_configuration_struct import GameConfigurationStruct
from ..game.game_struct import GameStruct
from .tournament_struct import TournamentStruct

@login_required
def create_tournament_game(request: HttpRequest, idplayer1:int, idplayer2: int, tournament: TournamentStruct) -> HttpResponse:

    player1 = CustomUser.objects.get(id=idplayer1)
    player2 = CustomUser.objects.get(id=idplayer2)
    game_name = f'{player1.username} vs {player2.username}'
    game_desc = f'Match du tournois {game_name} oposant {player1.username} et {player2.username}'
    game_struct = GameStruct(game_name, game_desc, tournament.game_configuration)
    game = construct_game(game_struct, construct_participate(idplayer1, idplayer2), tournament.id_tournament)

    return HttpResponse(f'/game?id={game.id_game}')