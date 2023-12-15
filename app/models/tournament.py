from django.db import models
from .custom_user import CustomUser
from .game_configuration import GameConfiguration
from datetime import datetime

class Tournament(models.Model):
    '''Classe permettant de creer un tournoi'''
    name = models.CharField(max_length=255)
    register_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    organisator = models.CharField(max_length=255)
    code = models.CharField(max_length=16)
    description = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    game_configuration = models.ForeignKey(GameConfiguration, on_delete=models.CASCADE, null=False)
    player_min = models.IntegerField()
    start = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    tournament_status = models.FileField(upload_to='dynamic/tournaments', null=True)

    def get_filename(self) -> str:
        return f'dynamic/tournaments/{self.id}.json'

    #Permet de verifier si le tournois est en cours
    def ongoing(self):
        ret = False

        if(self.start_date <= datetime.now().date() <= self.end_date):
            ret = True

        return ret

    def terminated(self):
        ret = False

        if(self.end_date <= datetime.now().date()):
            ret = True

        return ret

    def __str__(self):
        return self.name

class ParticipateTournament(models.Model):
    '''Classe permettant de creer une table qui répertorie les joueurs dans un tournoi'''
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    win = models.BooleanField(default=False)
