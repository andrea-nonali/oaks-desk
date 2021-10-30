from django.db import models
from django.db.models import Q


class PokemonStats(models.Model):
    pokemon = models.OneToOneField('Pokemon', null=False, on_delete=models.CASCADE, related_name='stats')
    hp = models.PositiveSmallIntegerField()
    attack = models.PositiveSmallIntegerField()
    sp_attack = models.PositiveSmallIntegerField()
    defense = models.PositiveSmallIntegerField()
    sp_defense = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()
    total_points = models.PositiveSmallIntegerField()

    @staticmethod
    def get_best_base_total_stats_pokemon_for_generation(generation: str) -> list:
        return list(
            PokemonStats.objects.filter(pokemon__generation=generation)
            .order_by('-total_points')
        )

    @staticmethod
    def get_best_base_total_stats_pokemon_for_type(type: str) -> list:
        return list(
            PokemonStats.objects.filter(Q(pokemon__type_1=type) | Q(pokemon__type_2=type))
            .order_by('-total_points')
        )

    @staticmethod
    def get_best_base_total_stats_pokemon_for_generation_and_type(generation: str, type: str) -> list:
        return list(
            PokemonStats.objects.filter(
                Q(pokemon__type_1=type) | Q(pokemon__type_2=type),
                pokemon__generation=generation
            )
            .order_by('-total_points')
        )
