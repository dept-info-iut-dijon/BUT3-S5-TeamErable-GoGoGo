from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from ..game.create_game import construct_game, construct_participate
from ...models import CustomUser
from ..game.game_struct import GameStruct
from .tournament_struct import TournamentStruct

@login_required
def create_tournament_game(request: HttpRequest, idplayer1:int, idplayer2: int, tournament: TournamentStruct) -> HttpResponse:
    '''Fonction permettant de creer une nouvelle partie dans le tournoi

    Args:
        request (HttpRequest): Requête HTTP
        idplayer1 (int): L'id du premier joueur
        idplayer2 (int): L'id du deuxième joueur
        tournament (TournamentStruct): Le tournoi

    Returns:
        HttpResponse: La requête HTTP
    '''
    player1 = CustomUser.objects.get(id=idplayer1)
    player2 = CustomUser.objects.get(id=idplayer2)
    game_name = f'{player1.username} vs {player2.username}'
    game_desc = f'Match du tournois {game_name} oposant {player1.username} et {player2.username}'
    game_struct = GameStruct(game_name, game_desc, tournament.game_configuration)
    game = construct_game(game_struct, construct_participate(idplayer1, idplayer2), tournament.id_tournament)

    return HttpResponse(f'/game?id={game.id_game}')