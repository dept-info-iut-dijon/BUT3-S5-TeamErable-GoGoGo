from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from ..models import Game
from ..logic import Board, Tile, RuleFactory, Vector2
from ..exceptions import InvalidMoveException

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
            assert data['type']
            assert data['data']

            match data['type']:
                case 'connect':
                    self.receive_connect(data)

                case 'disconnect':
                    self.receive_disconnect(data)

                case 'play':
                    self.receive_play(data)

        except (InvalidMoveException, ValueError) as e:
            self.send(text_data = json.dumps({'type': 'error', 'data': str(e)}))

        except: pass


    def disconnect(self, code: int) -> None:
        '''Déconnecte le joueur de la partie.

        Args:
            code (int): Code de déconnexion.
        '''
        async_to_sync(self.channel_layer.group_discard)(f'game_{self._game_id}', self.channel_name)
        self.close()


    def receive_play(self, event: dict) -> None:
        '''Reçoit le coup du joueur.

        Args:
            event (dict): Coup du joueur.
        '''
        data: str = event['data']

        x, y = data.split(';')
        x = int(x); y = int(y)

        game = Game.objects.get(id_game = self._game_id)

        board = Board(game.game_configuration.map_size, RuleFactory().get(game.game_configuration.counting_method))
        with open(game.move_list.path, 'r') as f:
            board.load(json.load(f))

        tile = Tile.White if self._player_id == 0 else Tile.Black
        ret = board.play(Vector2(x, y), tile)
        parsed_ret = {}
        for key, value in ret.items():
            k = 'w' if key == Tile.White else 'b' if key == Tile.Black else 'r'
            value = [f'{v.x};{v.y}' for v in value]
            parsed_ret[k] = '\n'.join(value)

        with open(game.move_list.path, 'w') as f:
            json.dump(board.export(), f)

        new_event = {'type': 'send_play', 'data': json.dumps(parsed_ret)}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)

        new_event = {'type': 'send_can_play', 'data': 0 if board.current_player == Tile.White else 1}
        async_to_sync(self.channel_layer.group_send)(f'game_{self._game_id}', new_event)


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


    def receive_connect(self, event: dict) -> None:
        '''Reçoit la connexion du joueur.

        Args:
            event (dict): Connexion du joueur.
        '''
        data: str = event['data']
        self.send(text_data = json.dumps(event))


    def receive_disconnect(self, event: dict) -> None:
        '''Reçoit la déconnexion du joueur.

        Args:
            event (dict): Déconnexion du joueur.
        '''
        data: str = event['data']
        print('disconnect', data)
        self.send(text_data = json.dumps(event))
