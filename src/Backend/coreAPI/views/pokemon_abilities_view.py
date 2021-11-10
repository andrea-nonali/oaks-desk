from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.serializers import PokemonAbilitySerializer
from coreAPI.views.utils import get_pokemon


class PokemonAbilitiesAPI(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse([
                PokemonAbilitySerializer(ability).data
                for ability in pokemon.get_abilities()
            ],
            safe=False
        )