from django.db import models
from .custom_user import CustomUser

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    register_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    organisator = models.CharField(max_length=255)
    code = models.IntegerField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Participate(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trounament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    win = models.BooleanField(default=False)