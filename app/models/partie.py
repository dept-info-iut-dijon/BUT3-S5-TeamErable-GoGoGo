from django.db import models
from .person import CustomUser

class Partie(models.Model):
    idPartie = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=16, null=True)
    dateDebut = models.DateField()
    duree = models.IntegerField()
    termine = models.BooleanField(default=False)
    joueur1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='joueur1')
    joueur2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='joueur2', null=True)