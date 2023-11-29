from dataclasses import dataclass
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
