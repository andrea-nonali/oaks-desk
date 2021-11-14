from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonSerializer


class PokemonDataAPI(APIView):
    def get(self, request):
        return JsonResponse(
            PokemonSerializer(
                Pokemon.get_pokemon(self.request.GET.get('pokemon-id'))
            ).data,
            safe=False
        )
