from dataclasses import dataclass
from .game_configuration_struct import GameConfigurationStruct

@dataclass
class GameStruct:
    name : str
    description : str
    game_configuration : GameConfigurationStruct