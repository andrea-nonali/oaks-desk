from django.http import JsonResponse, Http404
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonSerializer, PokemonAbilitySerializer


def get_pokemon(request):
    pokemon = Pokemon.get_pokemon(request.GET.get('pokedex_number'))
    if not pokemon:
        return Http404()
    return pokemon


class PokemonStatsAPIView(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse(
            pokemon.get_stats(),
            safe=False
        )


class PokemonAbilitiesAPI(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        abilities = [
            PokemonAbilitySerializer(ability).data
            for ability in pokemon.get_abilities()
        ]

        return JsonResponse(
            abilities,
            safe=False
        )


class WeakAgainstAPI(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse(
            pokemon.get_weak_types_against(),
            safe=False,
        )


class StrongAgainstAPI(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse(
            pokemon.get_strong_types_against(),
            safe=False,
        )


class NeutralAgainstAPI(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse(
            pokemon.get_neutral_types_against(),
            safe=False,
        )


class CoveringPokemonsAPI(APIView):

    def get(self, request):
        pokemon = get_pokemon(request)

        covering_pokemons = [
            PokemonSerializer(pokemon).data
            for pokemon in pokemon.get_fully_covering_pokemons(self.request.GET.get('generation'))
        ]

        return JsonResponse(
            covering_pokemons,
            safe=False
        )


class MegaEvolutionsAPI(APIView):
    def get(self, request):
        generation = self.request.GET.get('generation')

        if generation:
            pokemons = Pokemon.objects.filter(generation=generation)
        else:
            pokemons = Pokemon.objects.all()

        mega_pokemons = [
            PokemonSerializer(pokemon.get_mega_evolution()).data
            for pokemon in pokemons
            if pokemon.has_mega_evolution()
        ]

        return JsonResponse(
            mega_pokemons,
            safe=False
        )
