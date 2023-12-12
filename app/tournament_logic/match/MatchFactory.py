from .Match import Match
from .FakeMatch import FakeMatch
from .IMatch import IMatch
from ..Player import Player

class MatchFactory:
    def __new__(cls) -> None:
        return None


    @staticmethod
    def build_match(*players: Player) -> IMatch:
        res = None

        match len(players):
            case 0: raise ValueError('No players')
            case 1: res = FakeMatch(players[0])
            case 2: res = Match(players[0], players[1])
            case _: raise ValueError('Invalid number of players')

        return res
