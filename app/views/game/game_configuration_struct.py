from dataclasses import dataclass

@dataclass
class GameConfigurationStruct:
    is_private : bool
    ranked : bool
    map_size : str
    counting_method : str
    byo_yomi : str
    clock_type : str
    time_clock : str
    komi : str
    handicap : str

