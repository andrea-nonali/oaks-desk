from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.serializers import PokemonStatsSerializer
from coreAPI.views.utils import get_pokemon


class PokemonStatsAPIView(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse(
            PokemonStatsSerializer(pokemon.get_stats()).data,
            safe=False
        )