from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from coreAPI.models import Pokemon, PokemonAbilities
from coreAPI.serializers import PokemonAbilitySerializer


class PokemonAbilitiesAPI(APIView):
    def get(self, request):
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse(
            PokemonAbilitySerializer(
                PokemonAbilities.objects.get(pokemon=pokemon)
            ).data,
            safe=False
        )
