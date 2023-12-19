from ...models import Game, GameSave
from ...logic import Board, Tile
from ...views.tournament.tournament_game import update_tournament_games
from ...storage import TournamentStorage, GameStorage
from ...tournament_logic import Player


def _update_tournament_data(game: Game, board: Board) -> None:
    if game.tournament is not None:
        tournament_logic = TournamentStorage.load_tournament(game.tournament.tournament_status.path)
        points = board.get_points()
        winner = game.game_participate.player1 if points[Tile.White] > points[Tile.Black] else game.game_participate.player2
        tournament_logic.do_win(Player(winner.id))
        TournamentStorage.save_tournament(game.tournament.tournament_status.path, tournament_logic)
        update_tournament_games(game.tournament)


def _delete_game(game: Game) -> None:
    path = game.move_list.path
    GameStorage.delete_game(path)
    game.delete()


def _convert_game_to_game_save(game: Game, board: Board) -> None:
    try:
        players = (game.game_participate.player1, game.game_participate.player2)
        points = board.get_points()
        for player in players:
            GameSave.objects.create(
                id_game_save = game.id_game,
                user = player,
                name = game.name,
                player1 = game.game_participate.player1,
                player2 = game.game_participate.player2,
                score_player1 = points[Tile.White],
                score_player2 = points[Tile.Black],
                duration = game.duration,
                move_list = '\n'.join([move.export() for move in board._history]),
                tournament = game.tournament,
                map_size = game.game_configuration.map_size,
                komi = game.game_configuration.komi,
                counting_method = game.game_configuration.counting_method,
                clock_type = game.game_configuration.clock_type,
                clock_value = game.game_configuration.clock_value,
                byo_yomi = game.game_configuration.byo_yomi,
                handicap = game.game_configuration.handicap,
            )

            _delete_game(game)

    except Exception as e:
        print(e)


def end_of_game_callback(game: Game, board: Board) -> None:
    _update_tournament_data(game, board)
    _convert_game_to_game_save(game, board)
