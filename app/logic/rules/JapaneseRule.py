from ..RuleBase import RuleBase, Board, Tile
from ..RuleFactory import RuleFactory

class JapaneseRule(RuleBase):
    '''Règle japonaise.'''

    key: str = 'japanese'

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def count_points(board: Board) -> dict[Tile, int]:
        '''Compte les points selon la règle japonaise.

        On compte seulement les territoires.

        Args:
            board (Board): Plateau de jeu.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        pass # todo: implement this method



RuleFactory().register(JapaneseRule)
