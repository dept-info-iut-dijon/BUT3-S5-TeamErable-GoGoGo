from dataclasses import dataclass
from ...http import verify_post, verify_game_config
from django.http import HttpRequest
from typing import Union
from ..game.game_configuration_struct import GameConfigurationStruct

@dataclass
class TournamentStruct:
    name : str
    start_date : str
    end_date : str
    organisator : str
    description : str
    player_min : str
    game_configuration : GameConfigurationStruct

    @classmethod
    def verify_tournament(cls, request: HttpRequest) -> Union["TournamentStruct", Exception]:
        ret = None
        try: 
            game_config = verify_game_config(request)
            ret = cls(
                name = verify_post(request, 'tournament-name', 'Le nom du tournoi est vide.'),
                start_date = verify_post(request, 'start-date', 'La date de début du tournoi est vide.'),
                end_date = verify_post(request, 'end-date', 'La date de fin du tournoi est vide.'),
                organisator = verify_post(request, 'tournament-organizer', 'L\'organisateur du tournoi est vide.'),
                description = verify_post(request, 'tournament-desc', 'La description du tournoi est vide.'),
                player_min = verify_post(request, 'tournament-player-min', 'Le nombre de joueurs minimum est vide.'),
                game_configuration = game_config
            )
        except Exception as e:
            ret = e
        return ret

    def __str__(self):
        return (f"TournamentStruct(name={self.name}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"organisator={self.organisator}, "
                f"description={self.description}, "
                f"player_min={self.player_min}) ")
