from interface import Interface
from ..Player import Player

class IMatch(Interface):
    @property
    def winner(self) -> Player | None:
        pass


    def do_win(self, player: Player) -> None:
        pass


    def get_current_matches(self) -> list['IMatch']:
        pass
