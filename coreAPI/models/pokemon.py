from django.db import models

POKEMON_STATUS = {
    'normal': 'Normal',
    'sub_legendary': 'Sub Legendary',
    'legendary': 'Legendary',
    'mythical': 'Mythical'
}

POKEMON_STATUS_CHOICES = [
    (POKEMON_STATUS['normal'], POKEMON_STATUS['normal']),
    (POKEMON_STATUS['sub_legendary'], POKEMON_STATUS['sub_legendary']),
    (POKEMON_STATUS['legendary'], POKEMON_STATUS['legendary']),
    (POKEMON_STATUS['mythical'], POKEMON_STATUS['mythical'])
]


class Pokemon(models.Model):
    pokedex_number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    japanese_name = models.CharField(max_length=50)
    generation = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=50, choices=POKEMON_STATUS_CHOICES)
    species = models.CharField(max_length=50)
    type_1 = models.CharField(max_length=50)
    type_2 = models.CharField(max_length=50)
    height_m = models.FloatField()
    weight_kg = models.FloatField(max_length=50)

    def __str__(self):
        return f'#{self.pokedex_number} {self.name} - {self.japanese_name}'

    @staticmethod
    def get_pokemon(pokedex_number):
        return Pokemon.objects.filter(pokedex_number=pokedex_number).first()

    @staticmethod
    def get_pokemon_by_name(name):
        return Pokemon.objects.filter(name__icontains=name).first()

    @staticmethod
    def get_pokemons_for(generation=None):
        if generation:
            return Pokemon.objects.filter(generation=generation).all()
        return Pokemon.objects.all()

    def has_mega_evolution(self):
        pokemon = Pokemon.objects.filter(pokedex_number=self.pokedex_number)
        return pokemon.count() > 1 \
               and 'mega' in pokemon[1].name.lower() \
               and not self.is_mega_evolution()

    def is_mega_evolution(self):
        return 'mega' in self.name.lower()

    def get_mega_evolution(self):
        if self.has_mega_evolution():
            return Pokemon.objects.filter(pokedex_number=self.pokedex_number).all()[1]

    def get_abilities(self) -> []:
        return list(self.abilities.filter(pokemon=self))

    def get_stats(self) -> {}:
        return self.stats

    def get_strong_types_against(self) -> {}:
        return self.type_intersections.get_strong_types_against()

    def get_weak_types_against(self) -> {}:
        return self.type_intersections.get_weak_types_against()

    def get_neutral_types_against(self) -> {}:
        return self.type_intersections.get_neutral_types_against()

    def get_fully_covering_pokemons(self, generation=None):
        weaknesses = self.get_weak_types_against().keys()

        return [
            pokemon_to_compare
            for pokemon_to_compare in Pokemon.get_pokemons_for(generation)
            if set(weaknesses) <= set(pokemon_to_compare.get_strong_types_against().keys())
        ]
