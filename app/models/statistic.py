from django.db import models

class Statistic(models.Model):
    game_win = models.IntegerField()
    game_loose = models.IntegerField()
    game_ranked_win = models.IntegerField()
    game_ranked_loose = models.IntegerField()






