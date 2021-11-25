from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonAbilitySerializer


class PokemonAbilitiesAPI(APIView):
    def get(self, request):
        pokemon = Pokemon.get_pokemon_by_id(self.request.GET.get('pokemon_id'))

        return JsonResponse([
                PokemonAbilitySerializer(ability).data
                for ability in pokemon.get_abilities()
            ],
            safe=False
        )