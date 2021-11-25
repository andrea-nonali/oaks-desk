from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonSerializer


class WeakAgainstAPI(APIView):
    def get(self, request):
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse(
            pokemon.type_intersections.get_weak_types_against(),
            safe=False,
        )


class StrongAgainstAPI(APIView):
    def get(self, request):
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse(
            pokemon.type_intersections.get_strong_types_against(),
            safe=False,
        )


class NeutralAgainstAPI(APIView):
    def get(self, request):
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse(
            pokemon.type_intersections.get_neutral_types_against(),
            safe=False,
        )


class CoveringPokemonsAPI(APIView):

    def get(self, request):
        generation = self.request.GET.get('generation')
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse([
                PokemonSerializer(pokemon).data
                for pokemon in pokemon.type_intersections.get_fully_covering_pokemons(generation)
            ],
            safe=False
        )