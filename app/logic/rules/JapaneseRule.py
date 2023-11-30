from ..RuleBase import RuleBase, Board, Tile
from ..RuleFactory import RuleFactory

class JapaneseRule(RuleBase):
    '''Règle japonaise.'''

    key: str = 'japanese'

    def __init__(self, board: Board) -> None:
        super().__init__(board)

    def count_points(self) -> dict[Tile, float]:
        '''Compte les points selon la règle japonaise.

        On compte seulement les territoires.
        Les pionts du joueur b qui sont dans les territoires du joueur a, sont soustrait pour le score du joueur b.
        Les cases vides compris dans le territoire du joueur a sont ajoutés pour le score du joueur a.

        Returns:
            dict[Tile, int]: Points des joueurs.
        '''
        territories = self.board.get_territories()

        death_pionts_black = 0
        death_pionts_white = 0
        score_black = 0
        score_white = 0

        for t in territories:
            for territory in territories[t]:
                for pion in territory.coords:
                    if territory.tile == Tile.White:
                        if self.board.get(pion) == Tile.Black: 
                            death_pionts_black += 1

                        if self.board.get(pion) == None: 
                            score_white += 1

                    if territory.tile == Tile.Black:
                        if self.board.get(pion) == Tile.White: 
                            death_pionts_white += 1

                        if self.board.get(pion) == None: 
                            score_black += 1

        print(score_black, score_white, death_pionts_black, death_pionts_white, self.board.komi)
        score_black -= death_pionts_black
        score_white -= death_pionts_white
        score_black += self.board.komi

        return {
            Tile.Black: score_black,
            Tile.White: score_white
        }

RuleFactory().register(JapaneseRule)
