from django.db import models

class GameConfiguration(models.Model):
    id_game_config = models.AutoField(primary_key=True)
    is_private = models.BooleanField(default=False)
    ranked = models.BooleanField(default=False)
    map_size = models.IntegerField(null=False)
    komi = models.FloatField(null=False)
    counting_method = models.CharField(max_length=255, null=False)
    clock_type = models.CharField(max_length=255, null=False)
    clock_value = models.IntegerField(null=False)
    byo_yomi = models.IntegerField(null=False)
    handicap = models.IntegerField(null=True)