from interface import implements
from .IMatch import IMatch
from ..Player import Player

class Bracket(implements(IMatch)):
    def __init__(self, bracket1: IMatch, bracket2: IMatch) -> None:
        self._id: int = None
        self._bracket1 = bracket1
        self._bracket2 = bracket2
        self._winner: Player | None = None


    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if self._id is not None: raise Exception('Match id is already set')
        self._id = value

    @property
    def bracket1(self) -> IMatch:
        return self._bracket1

    @property
    def bracket2(self) -> IMatch:
        return self._bracket2

    @property
    def winner(self) -> Player | None:
        return self._winner


    def __str__(self) -> str:
        addon = ' -> Match' if self._bracket1.winner is not None and self._bracket2.winner is not None else ''
        s1 = '\t' + str(self._bracket1).replace('\n', '\n\t')
        s2 = '\t' + str(self._bracket2).replace('\n', '\n\t')
        return f'{__class__.__name__}{addon}(\n{s1},\n{s2}\n)'


    def do_win(self, player: Player) -> None:
        if (self._bracket1.winner is None): self._bracket1.do_win(player)
        elif (self._bracket2.winner is None): self._bracket2.do_win(player)
        else:
            if (self._bracket1.winner == player): self._winner = self._bracket1.winner
            elif (self._bracket2.winner == player): self._winner = self._bracket2.winner


    def get_current_matches(self) -> list[IMatch]:
        ret = []

        if (self._bracket1.winner is None): ret += self._bracket1.get_current_matches()
        if (self._bracket2.winner is None): ret += self._bracket2.get_current_matches()

        if self._bracket1.winner is not None and self._bracket2.winner is not None: ret.append(self)

        return ret
