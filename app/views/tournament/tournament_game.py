from ..game.create_game import construct_game, construct_participate
from ...models import CustomUser
from ..game.game_struct import GameStruct
from .tournament_struct import TournamentStruct
from random import shuffle
from ...models.game_participate import GameParticipate
from ...models.tournament import Tournament
from ...models.tournament import ParticipateTournament
from ..game.game_configuration_to_game_configuration_struct import game_configuration_to_game_configuration_struct
from ...tournament_logic import Tournament as TournamentLogic, Player as TournamentPlayer
from ...models.game import Game
from ...storage import TournamentStorage
from datetime import datetime


def start_tournament(tournament: Tournament, participants: list[CustomUser]) -> None:
    players = participants.copy()
    shuffle(players)

    tl = TournamentLogic([TournamentPlayer(p.id) for p in players])
    f = tournament.get_filename()

    matches = tl.get_current_matches()
    for match in matches:
        try:
            game = create_tournament_game(match.player1.id, match.player2.id, tournament)

            match.id = game.id

            TournamentStorage.save_tournament(tl, f)
            tournament.tournament_status = f

        except:
            pass


def create_tournament_game(id_player1: int, id_player2: int, tournament: Tournament) -> None:
    '''Fonction permettant de creer une nouvelle partie dans le tournoi

    Args:
        idplayer1 (int): L'id du premier joueur
        idplayer2 (int): L'id du deuxième joueur
        tournament (TournamentStruct): Le tournoi
    '''
    player1 = CustomUser.objects.get(id=id_player1)
    player2 = CustomUser.objects.get(id=id_player2)
    game_name = f'{player1.username} vs {player2.username}'
    game_desc = f'Match du tournois {game_name} oposant {player1.username} et {player2.username}'
    game_struct = GameStruct(
        game_name,
        game_desc,
        game_configuration_to_game_configuration_struct(tournament.game_configuration),
    )
    game = construct_game(game_struct, construct_participate(id_player1, id_player2), tournament.id)
    tournament_cls = Tournament.objects.get(id=tournament.id)


def update_tournament_games(tournament: Tournament) -> None:
    tournament_logic = TournamentStorage.load_tournament(tournament.tournament_status.path)
    matches = tournament_logic.get_current_matches()

    for match in matches:
        try:
            Game.objects.get(id=match.id)

        except Game.DoesNotExist:
            create_tournament_game(match.player1.id, match.player2.id, tournament)
