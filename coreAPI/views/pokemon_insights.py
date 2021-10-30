from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonSerializer


class MegaEvolutionsAPI(APIView):
    def get(self, request):
        generation = self.request.GET.get('generation')

        pokemons = Pokemon.get_pokemons_for(generation)

        mega_pokemons = [
            PokemonSerializer(pokemon.get_mega_evolution()).data
            for pokemon in pokemons
            if pokemon.has_mega_evolution()
        ]

        return JsonResponse(
            mega_pokemons,
            safe=False
        )
