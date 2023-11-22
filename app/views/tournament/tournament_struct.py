from dataclasses import dataclass

@dataclass
class TournamentStruct:
    name : str
    start_date : str
    end_date : str
    organisator : str
    description : str
    player_min : str
    map_size : str
    counting_method : str
    byo_yomi : str
    clock_type : str
    time_clock : str
    komi : str
    handicap : str
