from abc import ABC, abstractmethod
from .Tile import Tile
from . import Board


class RuleBase(ABC):
    '''Classe de base des règles de jeu.'''

    key: str = 'base'

    def __init__(self, board: Board) -> None:
        '''Initialise une règle de jeu.

        Args:
            board (Board): Plateau de jeu.
        '''
        self._board = board


    @abstractmethod
    def count_points(self) -> dict[Tile, int]:
        '''Compte les points.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        pass
