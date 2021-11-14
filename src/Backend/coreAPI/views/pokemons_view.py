from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonAbilitySerializer, PokemonSerializer
from coreAPI.views.utils import get_pokemon


class PokemonsAPI(APIView):
    def get(self, request):
        return JsonResponse([
                PokemonSerializer(pokemon).data
                for pokemon in Pokemon.objects.all()
            ],
            safe=False
        )