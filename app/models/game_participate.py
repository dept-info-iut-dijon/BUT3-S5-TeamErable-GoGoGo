from django.db import models
from .custom_user import CustomUser

class GameParticipate(models.Model):
    id_game_participate = models.AutoField(primary_key=True)
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player2', null=True)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()