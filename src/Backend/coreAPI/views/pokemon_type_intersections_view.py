from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonSerializer


class WeakAgainstAPI(APIView):
    def get(self, request):
        pokemon = Pokemon.get_pokemon_by_id(self.request.GET.get('pokemon_id'))

        return JsonResponse(
            pokemon.type_intersections.get_weak_types_against(),
            safe=False,
        )


class StrongAgainstAPI(APIView):
    def get(self, request):
        pokemon = Pokemon.get_pokemon_by_id(self.request.GET.get('pokemon_id'))

        return JsonResponse(
            pokemon.type_intersections.get_strong_types_against(),
            safe=False,
        )


class NeutralAgainstAPI(APIView):
    def get(self, request):
        pokemon = Pokemon.get_pokemon_by_id(self.request.GET.get('pokemon_id'))

        return JsonResponse(
            pokemon.type_intersections.get_neutral_types_against(),
            safe=False,
        )


class CoveringPokemonsAPI(APIView):

    def get(self, request):
        generation = self.request.GET.get('generation')
        pokemon = Pokemon.get_pokemon_by_id(self.request.GET.get('pokemon_id'))

        return JsonResponse([
                PokemonSerializer(pokemon).data
                for pokemon in pokemon.type_intersections.get_fully_covering_pokemons(generation)
            ],
            safe=False
        )