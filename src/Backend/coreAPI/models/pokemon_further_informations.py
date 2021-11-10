from django.db import models


class PokemonFurtherInformations(models.Model):
    pokemon = models.OneToOneField('Pokemon', null=False, on_delete=models.CASCADE, related_name='informations')
    catch_rate = models.PositiveSmallIntegerField()
    base_friendship = models.PositiveSmallIntegerField()
    base_experience = models.PositiveSmallIntegerField()
    growth_rate = models.CharField(max_length=50)
    egg_type_1 = models.CharField(max_length=20)
    egg_type_2 = models.CharField(max_length=20)
    percentage_male = models.FloatField()
    egg_cycles = models.PositiveSmallIntegerField()