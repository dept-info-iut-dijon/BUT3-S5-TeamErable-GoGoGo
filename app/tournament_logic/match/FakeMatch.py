from interface import implements
from .IMatch import IMatch
from ..Player import Player

class FakeMatch(implements(IMatch)):
    def __init__(self, player: Player) -> None:
        self._player = player


    @property
    def player(self) -> Player:
        return self._player

    @property
    def winner(self) -> Player | None:
        return self._player


    def __str__(self) -> str:
        return 'FakeMatch -> ' + str(self._player)


    def do_win(self, player: Player) -> None:
        pass


    def get_current_matches(self) -> list[IMatch]:
        return []
