from django.db import models

class Statistic(models.Model):
    '''Classe permettant de creer une table qui répertorie les statistiques des joueurs'''
    game_win = models.IntegerField()
    game_loose = models.IntegerField()
    game_ranked_win = models.IntegerField()
    game_ranked_loose = models.IntegerField()






