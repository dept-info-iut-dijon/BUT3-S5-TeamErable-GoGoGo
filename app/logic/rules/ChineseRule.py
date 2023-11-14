from ..RuleBase import RuleBase, Board, Tile
from ..RuleFactory import RuleFactory

class ChineseRule(RuleBase):
    '''Règle chinoise.'''

    key: str = 'chinese'

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def count_points(self) -> dict[Tile, int]:
        '''Compte les points selon la règle chinoise.

        On compte les territoires et les pierres qui dessinent les territoires.

        Args:
            board (Board): Plateau de jeu.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        pass # TODO: Implement this method



RuleFactory().register(ChineseRule)
