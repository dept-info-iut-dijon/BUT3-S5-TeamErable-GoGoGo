from abc import ABC, abstractmethod
from ..Tile import Tile
from .. import Board
from datetime import timedelta, datetime

class TimerBase(ABC):
    '''Classe abstraite pour le minuteur'''

    key: str = 'base'

    def __init__(self, board: Board, byo_yomi: int, initial_time: timedelta, player_time: dict[Tile, timedelta] | None, last_action_time: datetime | None) -> None:
        '''
        Methode du constructeur pour le minuteur

        Args :
            timer_data (dict): Dictionnaire contenant les donnees de configuration du minuteur.
        '''
        self._board = board
        self._byo_yomi = byo_yomi
        self._initial_time = timedelta(seconds = initial_time.total_seconds())
        self._player_time = player_time if player_time is not None else {t: timedelta(seconds = initial_time.total_seconds()) for t in Tile}
        self._last_action_time = last_action_time if last_action_time is not None else datetime.now()


    @property
    def board(self) -> Board:
        '''Plateau de jeu.

        Returns:
            Board: Plateau de jeu.
        '''
        return self._board

    @property
    def byo_yomi(self) -> int:
        '''Periode de byo-yomi.

        Returns:
            int: Periode de byo-yomi.
        '''
        return self._byo_yomi

    @property
    def initial_time(self) -> timedelta:
        '''Temps total.

        Returns:
            timedelta: Temps total.
        '''
        return self._initial_time

    @property
    def player_time(self) -> dict[Tile, timedelta]:
        '''Temps des joueurs.

        Returns:
            timedelta: Temps des joueurs.
        '''
        return self._player_time


    @property
    def last_action_time(self) -> datetime:
        '''Temps du dernier placement.

        Returns:
            datetime: Temps du dernier placement.
        '''
        return self._last_action_time


    @property
    def last_action_time_diff(self) -> timedelta:
        '''Temps depuis le dernier placement.

        Returns:
            timedelta: Temps depuis le dernier placement.
        '''
        return datetime.now() - self._last_action_time


    @property
    def timed_out(self) -> Tile | None:
        for t in Tile:
            if self._player_time[t] - self.last_action_time_diff <= timedelta(seconds = 0):
                return t
        return None


    def update_last_action_time(self) -> None:
        '''Met a jour le temps du dernier placement.'''
        self._last_action_time = datetime.now()


    def export(self) -> dict:
        '''Exporte les données du minuteur.

        Returns:
            dict: Données du minuteur.
        '''
        return {
            'key': self.key,
            'byo-yomi': self._byo_yomi,
            'initial-time': self._initial_time.total_seconds(),
            'player-time': {key.value.value: value.total_seconds() for key, value in self._player_time.items()},
            'last-action-time': self._last_action_time.timestamp(),
        }


    @abstractmethod
    def copy(self) -> 'TimerBase':
        '''Copie le minuteur.

        Returns:
            TimerBase: Copie du minuteur.
        '''
        pass


    @abstractmethod
    def play(self, tile: Tile) -> None:
        '''Joue un coup.

        Args:
            tile (Tile): Couleur du joueur.
        '''
        pass


    def add_time(self, tile: Tile, time: timedelta | float | int) -> None:
        '''Ajoute du temps a un joueur.

        Args:
            tile (Tile): Couleur du joueur.
            time (timedelta): Temps a ajouter.
        '''
        if isinstance(time, timedelta):
            self._player_time[tile] += time
        self._player_time[tile] += timedelta(seconds = time)
