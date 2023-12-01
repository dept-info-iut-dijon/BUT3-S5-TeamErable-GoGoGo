from abc import ABC, abstractmethod
from ..Tile import Tile
from .. import Board
from datetime import timedelta

class TimerBase(ABC):
    '''Classe abstraite pour le minuteur'''

    key: str = 'base'

    def __init__(self, board: Board, byo_yomi: int, time: timedelta, player_time: dict[Tile, timedelta] | None) -> None:
        '''
        Methode du constructeur pour le minuteur

        Args :
            timer_data (dict): Dictionnaire contenant les donnees de configuration du minuteur.
        '''
        self._board = board
        self._byo_yomi = byo_yomi
        self._time = time
        self._player_time = player_time if player_time is not None else {t: timedelta(seconds = time.total_seconds()) for t in Tile}


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
    def time(self) -> timedelta:
        '''Temps total.

        Returns:
            timedelta: Temps total.
        '''
        return self._time

    @property
    def player_time(self) -> dict[Tile, timedelta]:
        '''Temps des joueurs.

        Returns:
            timedelta: Temps des joueurs.
        '''
        return self._player_time


    @abstractmethod
    def set_move(self) -> None:
        '''Sauvegarde le temps du nouveau placement'''
        pass


    @abstractmethod
    def make_move(self, player: Tile) -> bool:
        '''
        Gere le calcul du temps pour chaque coup.

        Args :
            player (Tile): Le joueur effectuant le coup (Noir ou Blanc).

        Returns :
            bool: True si la partie est terminee, False sinon.
        '''
        pass

    @abstractmethod
    def get_initial_time(self) -> float:
        '''
            Permet d'obtenir le temps depuis le dernier coup

            Returns:
                float: le temps depuis le dernier coup
        '''
        pass

    @abstractmethod
    def get_separate_timers(self) -> tuple[int, int]:
        '''
            Permet d'obtenir l'etat des timers separes

            Returns:
                (int, int): Tuple contenant l'etat des timers blanc et noir
        '''
        pass

    def export(self) -> dict:
        '''Exporte les données du minuteur.

        Returns:
            dict: Données du minuteur.
        '''
        return {
            'key': self.key,
            'byo_yomi': self._byo_yomi,
            'time': self._time.total_seconds(),
            'player_time': {key.value.value: value.total_seconds() for key, value in self._player_time.items()}
        }
