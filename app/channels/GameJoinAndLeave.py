from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import Game
from ..logic import Board, Tile, RuleFactory, Vector2
from ..exceptions import InvalidMoveException
from ..storage import GameStorage

class GameJoinAndLeave(WebsocketConsumer):
    '''Gère le websocket de la partie.

    Args:
        WebsocketConsumer (_type_): Classe de base du websocket.
    '''

    def connect(self) -> None:
        '''Connecte le joueur à la partie.'''
        self._user = self.scope['user']
        self._game_id = self.scope['url_route']['kwargs']['game_id']

        game = Game.objects.get(id_game = self._game_id)
        self._player_id = 0 if game.game_participate.player1 == self._user else 1 if game.game_participate.player2 == self._user else -1
        if self._player_id == -1: return self.close()

        async_to_sync(self.channel_layer.group_add)(f'game_{self._game_id}', self.channel_name)

        self.accept()


    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        '''Reçoit les données du joueur.

        Args:
            text_data (str, optional): Données du joueur. Defaults to None.
            bytes_data (bytes, optional): Données du joueur. Defaults to None.
        '''
        try:
            data = json.loads(text_data)
            assert 'type' in data.keys()
            assert 'data' in data.keys()

            match data['type']:
                case 'connect':
                    self.receive_connect(data)

                case 'disconnect':
                    self.receive_disconnect(data)

                case 'play':
                    self.receive_play(data)

                case 'skip':
                    self.receive_skip(data)

                case 'give-up':
                    self.receive_give_up(data)

                case _:
                    raise ValueError('Une erreur est survenue.')

        except (InvalidMoveException, ValueError) as e:
            self.send(text_data = json.dumps({'type': 'error', 'data': str(e)}))

        except Exception as e:
            import traceback
            traceback.print_exc()


    def disconnect(self, code: int) -> None:
        '''Déconnecte le joueur de la partie.

        Args:
            code (int): Code de déconnexion.
        '''
        async_to_sync(self.channel_layer.group_discard)(f'game_{self._game_id}', self.channel_name)
        self.close()


    def _get_game_board(self) -> tuple[Game, Board, Tile]:
        game = Game.objects.get(id_game = self._game_id)

        board = GameStorage.load_game(game.move_list.path)

        return game, board, Tile.White if self._player_id == 0 else Tile.Black


    def _update_game(self, game: Game, board: Board) -> None:
        if board.ended != game.done:
            game.done = board.ended
            game.save()


    def _save_game_board(self, game: Game, board: Board) -> None:
        self._update_game(game, board)
        GameStorage.save_game(game.move_list.path, board)


    def _get_can_play(self, board: Board) -> int:
        can_play = 0 if board.current_player == Tile.White else 1
        can_play = -1 if board.ended else can_play
        return can_play


    def _check_end_game(self, game: Game, board: Board, looser: Tile = None) -> None:
        if board.ended:
            points = board.get_points()

            forfeit_value = looser.value.color[0] if looser is not None else None

            if forfeit_value:
                winner = looser.next

            else:
                winner, winner_points = None, 0
                for t in Tile:
                    if points[t] > winner_points: winner, winner_points = t, points[t]


            new_event = {
                'type': 'send_end_game',
                'data': json.dumps({
                    'winner': winner.value.color[0] if winner is not None else None,
                    'forfeit': forfeit_value,
                    'points': {
                        t.value.color[0]: {
                            'count': points[t], 'username': game.game_participate.player1.username if t == Tile.White else game.game_participate.player2.username
                        } for t in Tile
                    }
                })
            }
            async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


    def receive_play(self, event: dict) -> None:
        '''Reçoit le coup du joueur.

        Args:
            event (dict): Coup du joueur.
        '''
        data: str = event['data']

        x, y = data.split(';')
        x = int(x); y = int(y)

        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')

        ret = board.play(Vector2(x, y), tile)
        parsed_ret = {}
        for key, value in ret.items():
            k = 'r' if not key else key.value.color[0]
            value = [f'{v.x};{v.y}' for v in value]
            parsed_ret[k] = '\n'.join(value)

        self._save_game_board(game, board)

        new_event = {'type': 'send_play', 'data': json.dumps(parsed_ret)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_can_play', 'data': self._get_can_play(board)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_eaten_tiles', 'data': json.dumps({t.value.color[0]: board.get_eaten_tiles(t) for t in Tile})}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        self._check_end_game(game, board)


    def send_play(self, event: dict) -> None:
        '''Envoie le coup du joueur.

        Args:
            event (dict): Coup du joueur.
        '''
        new_event = {'type': 'play', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_can_play(self, event: dict) -> None:
        '''Envoie si le joueur peut jouer.

        Args:
            event (dict): Si le joueur peut jouer.
        '''
        new_event = {'type': 'can-play', 'data': event['data'] == self._player_id}
        self.send(text_data = json.dumps(new_event))


    def send_eaten_tiles(self, event: dict) -> None:
        '''Envoie les points du joueur.

        Args:
            event (dict): Les points du joueur.
        '''
        new_event = {'type': 'eaten-tiles', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def send_end_game(self, event: dict) -> None:
        '''Envoie la fin de la partie.

        Args:
            event (dict): La fin de la partie.
        '''
        new_event = {'type': 'end-game', 'data': event['data']}
        self.send(text_data = json.dumps(new_event))


    def receive_skip(self, event: dict) -> None:
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')

        board.play_skip(tile)

        self._save_game_board(game, board)

        new_event = {'type': 'send_can_play', 'data': self._get_can_play(board)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        self._check_end_game(game, board)


    def receive_give_up(self, event: dict) -> None:
        game, board, tile = self._get_game_board()
        if game.game_participate.player2 is None: raise InvalidMoveException('Vous ne pouvez pas jouer seul.')

        board.end_game()

        self._save_game_board(game, board)

        new_event = {'type': 'send_can_play', 'data': self._get_can_play(board)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        self._check_end_game(game, board, tile)


    def receive_connect(self, event: dict) -> None:
        '''Reçoit la connexion du joueur.

        Args:
            event (dict): Connexion du joueur.
        '''
        new_event = {'type': 'send_connect', 'data': {'id': self._user.id, 'color': 'white' if self._player_id == 0 else 'black'}}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


    def send_connect(self, event: dict) -> None:
        '''Envoie la connexion du joueur.

        Args:
            event (dict): Connexion du joueur.
        '''
        if self._user.id != event['data']['id']:
            new_event = {'type': 'connect', 'data': event['data']}
            self.send(text_data = json.dumps(new_event))


    def receive_disconnect(self, event: dict) -> None:
        '''Reçoit la déconnexion du joueur.

        Args:
            event (dict): Déconnexion du joueur.
        '''
        data: str = event['data']
        print('disconnect', data)
        self.send(text_data = json.dumps(event))
