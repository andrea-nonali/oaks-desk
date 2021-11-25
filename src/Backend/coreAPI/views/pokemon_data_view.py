from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonSerializer


class PokemonDataAPI(APIView):
    def get(self, request):
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse(
            PokemonSerializer(pokemon).data,
            safe=False
        )
