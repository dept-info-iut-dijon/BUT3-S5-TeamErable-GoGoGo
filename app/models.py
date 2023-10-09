from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Personne(models.Model):
    
    compte = models.OneToOneField(User, on_delete=models.CASCADE)

    amis = models.ManyToManyField('self', blank=True)

    def __self__(self):
        return self.nom