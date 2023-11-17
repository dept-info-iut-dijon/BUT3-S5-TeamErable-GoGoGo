from ..RuleBase import RuleBase, Board, Tile
from ..RuleFactory import RuleFactory
from .rules import JapaneseRule

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
        
        total = JapaneseRule.count_points(self.board)

        for x in range(self.board.size.x):
            for y in range(self.board.size.y):
                if self.board.get(Vector2(x, y)) == Tile.Black:
                    total[Tile.Black] += 1
                if self.board.get(Vector2(x, y)) == Tile.White:
                    total[Tile.White] += 1

        return total





RuleFactory().register(ChineseRule)
