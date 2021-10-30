from django.db import models


class PokemonTypeIntersections(models.Model):
    pokemon = models.OneToOneField('Pokemon', null=False, on_delete=models.CASCADE, related_name='type_intersections')
    against_bug = models.FloatField()
    against_dark = models.FloatField()
    against_dragon = models.FloatField()
    against_electric = models.FloatField()
    against_fairy = models.FloatField()
    against_fight = models.FloatField()
    against_fire = models.FloatField()
    against_flying = models.FloatField()
    against_ghost = models.FloatField()
    against_grass = models.FloatField()
    against_ground = models.FloatField()
    against_ice = models.FloatField()
    against_normal = models.FloatField()
    against_poison = models.FloatField()
    against_psychic = models.FloatField()
    against_rock = models.FloatField()
    against_steel = models.FloatField()
    against_water = models.FloatField()

    def get_weak_types_against(self) -> {}:
        return {
            'pokemon': self.pokemon.name
        } | {
            against: value
            for against, value in self._to_dict().items()
            if value > 1
        }

    def get_strong_types_against(self) -> {}:
        return {
            'pokemon': self.pokemon.name
        } | {
            against: value
            for against, value in self._to_dict().items()
            if value < 1
        }

    def get_neutral_types_against(self) -> {}:
        return {
            'pokemon': self.pokemon.name
       } | {
            against: value
            for against, value in self._to_dict().items()
            if value == 1
       }

    def _to_dict(self) -> {}:
        return {
            "against_bug": self.against_bug,
            "against_dark": self.against_dark,
            "against_dragon": self.against_dragon,
            "against_electric": self.against_electric,
            "against_fairy": self.against_fairy,
            "against_fight": self.against_fight,
            "against_fire": self.against_fire,
            "against_flying": self.against_flying,
            "against_ghost": self.against_ghost,
            "against_grass": self.against_grass,
            "against_ground": self.against_ground,
            "against_ice": self.against_ice,
            "against_normal": self.against_normal,
            "against_poison": self.against_poison,
            "against_psychic": self.against_psychic,
            "against_rock": self.against_rock,
            "against_steel": self.against_steel,
            "against_water": self.against_water
        }