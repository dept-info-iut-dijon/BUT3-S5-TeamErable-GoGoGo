from dataclasses import dataclass

@dataclass
class StatsStruct:
    total_tournaments : int
    total_wins_tournaments : int
    total_loses_tournaments : int
    total_games : int
    total_games_wins : int
    total_games_loses : int
    total_ranked_games : int
    total_ranked_wins : int
    total_ranked_loses : int
    elo : int
    rank : str
