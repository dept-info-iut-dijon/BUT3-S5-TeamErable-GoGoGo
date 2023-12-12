from .match.Bracket import Bracket
from .match.MatchFactory import MatchFactory
from .match.IMatch import IMatch
from .Player import Player

class Tournament:
    def __init__(self, *players: Player):
        self._players = list(players)
        self._bracket = self._generate_bracket(self._players)


    @property
    def players(self) -> list[Player]:
        return self._players

    @property
    def bracket(self) -> IMatch:
        return self._bracket


    def _generate_bracket(self, players: list[Player]) -> IMatch:
        ret = None

        length = len(players)
        if length <= 2: ret = MatchFactory.build_match(*players)
        else: ret = Bracket(self._generate_bracket(players[:length // 2]), self._generate_bracket(players[length // 2:]))

        return ret


    def __str__(self) -> str:
        s = '\t' + str(self._bracket).replace('\n', '\n\t')
        return f'{__class__.__name__}(\n{s}\n)'.replace('\t', ' ' * 4)


    def __repr__(self) -> str:
        return str(self)


    def do_win(self, player: Player) -> None:
        self._bracket.do_win(player)


    def get_current_matches(self) -> list[IMatch]:
        return self._bracket.get_current_matches()
