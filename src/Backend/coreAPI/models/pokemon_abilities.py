from django.db import models


class PokemonAbilities(models.Model):
    pokemon = models.ForeignKey('Pokemon', null=False, on_delete=models.CASCADE, related_name='abilities')
    ability_1 = models.CharField(max_length=50)
    ability_2 = models.CharField(max_length=50)
    ability_hidden = models.CharField(max_length=50)

    def __str__(self):
        return f'[{self.ability_1} - {self.ability_2} - {self.ability_hidden}]'

