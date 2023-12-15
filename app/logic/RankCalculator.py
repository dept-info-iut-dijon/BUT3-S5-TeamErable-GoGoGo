from .GoRank import GoRank

class RankCalculator:
    
    @staticmethod
    def calculate_rank(nb_games:int, win_rate:float)->str:
        WINRATE_TOLERANCE = 0.7
        STEP_INCREMENT = 5
        rank = 0
        step = STEP_INCREMENT
        nb_games_count = nb_games
        while nb_games_count > 0 and win_rate > 0 and rank < 39:
            win_rate -= (step*100/nb_games)*WINRATE_TOLERANCE
            nb_games_count -= step
            rank += 1
            if (rank/10).is_integer():
                step += STEP_INCREMENT
        return str(GoRank(rank))