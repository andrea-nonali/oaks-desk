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
    def get_best_base_total_stats_pokemon_for_generation(
            generation: str,
            include_legendaries=True,
            include_mythicals=True,
            include_mega_evolutions=True
    ) -> list:
        available_statuses = [POKEMON_STATUS['normal'], POKEMON_STATUS['sub_legendary']]
        if include_legendaries:
            available_statuses.append(include_legendaries)
        if include_mythicals:
            available_statuses.append(include_mythicals)
        if include_mega_evolutions:
            available_statuses.append(include_mega_evolutions)

        return list(
            PokemonStats.objects.filter(pokemon__generation=generation, pokemon__status__in=available_statuses)
            .order_by('-total_points')
        )

    @staticmethod
    def get_best_base_total_stats_pokemon_for_type(
            type: str,
            include_legendaries=True,
            include_mythicals=True,
            include_mega_evolutions=True
    ) -> list:
        available_statuses = [POKEMON_STATUS['normal'], POKEMON_STATUS['sub_legendary']]
        if include_legendaries:
            available_statuses.append(include_legendaries)
        if include_mythicals:
            available_statuses.append(include_mythicals)
        if include_mega_evolutions:
            available_statuses.append(include_mega_evolutions)

        return list(
            PokemonStats.objects.filter(Q(pokemon__type_1=type) | Q(pokemon__type_2=type))
            .order_by('-total_points')
        )

    @staticmethod
    def get_best_base_total_stats_pokemon_for_generation_and_type(
            generation: str,
            type: str,
            include_legendaries=True,
            include_mythicals=True,
            include_mega_evolutions=True
    ) -> list:
        available_statuses = [POKEMON_STATUS['normal'], POKEMON_STATUS['sub_legendary']]
        if include_legendaries:
            available_statuses.append(include_legendaries)
        if include_mythicals:
            available_statuses.append(include_mythicals)
        if include_mega_evolutions:
            available_statuses.append(include_mega_evolutions)

        return list(
            PokemonStats.objects.filter(
                Q(pokemon__type_1=type) | Q(pokemon__type_2=type),
                pokemon__generation=generation
            )
            .order_by('-total_points')
        )
