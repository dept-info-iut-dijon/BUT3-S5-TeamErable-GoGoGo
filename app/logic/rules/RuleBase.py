from abc import ABC, abstractmethod
from ..Tile import Tile
from .. import Board


class RuleBase(ABC):
    '''Classe de base des règles de jeu.'''

    key: str = 'base'

    def __init__(self, board: Board, komi: float) -> None:
        '''Initialise une règle de jeu.

        Args:
            board (Board): Plateau de jeu.
        '''
        self._board = board
        self._komi = komi


    @property
    def board(self) -> Board:
        '''Plateau de jeu.

        Returns:
            Board: Plateau de jeu.
        '''
        return self._board

    @property
    def komi(self) -> float:
        '''Komi.

        Returns:
            float: Komi.
        '''
        return self._komi


    @abstractmethod
    def count_points(self) -> dict[Tile, float]:
        '''Compte les points.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        pass


    def export(self) -> dict:
        '''Exporte les données de la règle de jeu.

        Returns:
            dict: Données de la règle de jeu.
        '''
        return {
            'key': self.key,
            'komi': self.komi,
        }
