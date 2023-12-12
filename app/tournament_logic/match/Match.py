from interface import implements
from .IMatch import IMatch
from ..Player import Player

class Match(implements(IMatch)):
    def __init__(self, player1: Player, player2: Player) -> None:
        self._player1: Player = player1
        self._player2: Player = player2
        self._winner: Player = None


    @property
    def player1(self) -> Player:
        return self._player1

    @property
    def player2(self) -> Player:
        return self._player2

    @property
    def winner(self) -> Player | None:
        return self._winner


    def __str__(self) -> str:
        ret = ''
        if self._winner is not None:
            ret = str(self._winner)

        else:
            s1 = '\t' + str(self._player1).replace('\n', '\n\t')
            s2 = '\t' + str(self._player2).replace('\n', '\n\t')
            ret = f'{__class__.__name__}(\n{s1},\n{s2}\n)'

        return ret


    def do_win(self, player: Player) -> None:
        if player == self._player1: self._winner = self._player1
        elif player == self._player2: self._winner = self._player2


    def get_current_matches(self) -> list[IMatch]:
        return [self]
