from django.db import models
from django.db.models import Q

from coreAPI.models.pokemon import POKEMON_STATUS


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
    def get_best_base_total_stats_pokemon_for(
            generation='',
            type='',
            include_legendaries=True,
            include_mythicals=True,
    ) -> list:
        filters = PokemonStats._get_filters(generation, type)
        available_statuses = PokemonStats._get_available_statuses_list(include_legendaries, include_mythicals)

        return PokemonStats.objects.filter(
            filters,
            pokemon__status__in=available_statuses
        ).all().order_by('-total_points')

    @staticmethod
    def _get_filters(generation, type):
        filters = Q()
        if generation:
            filters |= Q(pokemon__generation=generation)
        if type:
            filters |= Q(Q(pokemon__type_1=type) | Q(pokemon__type_2=type))
        return filters

    @staticmethod
    def _get_available_statuses_list(include_legendaries, include_mythicals) -> []:
        available_statuses = [POKEMON_STATUS['normal'], POKEMON_STATUS['sub_legendary']]
        if include_legendaries:
            available_statuses.append(POKEMON_STATUS['legendary'])
        if include_mythicals:
            available_statuses.append(POKEMON_STATUS['mythical'])
        return available_statuses

