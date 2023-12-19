from .GoRank import GoRank

class RankCalculator:
    
    @staticmethod
    def calculate_rank(nb_games:int, win_rate:float)->str:
        '''Calcule le rang en fonction du nombre de parties et du taux de victoires

            Args:
                nb_games (int): le nombre de parties du joueur
                win_rate (int): le taux de victoire du joueur

            Returns:
                (str): le rang                
        '''
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

        if rank == 0 : rank = 1
        return str(GoRank(rank))

    @staticmethod
    def calculate_elo(winner_elo: int, loser_elo: int, k_factor=32)->tuple[int, int]:
        """
        Calcule les nouveaux elos de chaque joueurs

        Args:
            winner_elo (int): Le elo du gagnant
            loser_elo (int): Le elo du perdant
            k_factor (int): Le facteur k permettant de calculer le elo (par defaut 32)

        Returns:
            int, int: Les nouveaux elos
        """
        expected_win = 1 / (1 + 10**((loser_elo - winner_elo) / 400))
        expected_lose = 1 / (1 + 10**((winner_elo - loser_elo) / 400))

        updated_winner_elo = winner_elo + k_factor * (1 - expected_win)
        updated_loser_elo = loser_elo + k_factor * (0 - expected_lose)

        return int(updated_winner_elo), int(updated_loser_elo)