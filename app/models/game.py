from django.db import models
from .custom_user import CustomUser
from .tournament import Tournament

class Game(models.Model):
    id_game = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=16, null=True)
    start_date = models.DateField()
    duration = models.IntegerField()
    done = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament', null=True)
    player1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player2', null=True)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='winner', null=True)
