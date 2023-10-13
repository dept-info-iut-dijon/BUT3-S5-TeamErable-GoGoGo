from django.db import models
from .person import CustomUser

class Tournoi(models.Model):
    Nom = models.CharField(max_length=255)
    DateInscription = models.DateField()
    DateDebut = models.DateField()
    DateFin = models.DateField()
    Organisateur = models.CharField(max_length=255)
    Code = models.IntegerField(max_length=25)
    Gagnant = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Participer(models.Model):
    personne = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournoi = models.ForeignKey(Tournoi, on_delete=models.CASCADE)
    