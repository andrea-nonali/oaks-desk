from django.http import JsonResponse
from rest_framework.views import APIView

from coreAPI.models import PokemonStats
from coreAPI.serializers import PokemonStatsSerializer
from coreAPI.views.utils import get_pokemon


class PokemonStatsAPI(APIView):
    def get(self, request):
        pokemon = get_pokemon(request)

        return JsonResponse(
            PokemonStatsSerializer(pokemon.get_stats()).data,
            safe=False
        )


class BestPokemonAPIView(APIView):
    def get(self, request):
        generation = self.request.GET.get('generation')
        type = self.request.GET.get('type')
        include_legendaries = False if self.request.GET.get('include_legendaries') == 'False' else True
        include_mythicals = False if self.request.GET.get('include_mythicals') == 'False' else True

        pokemon_stats = PokemonStats.get_best_base_total_stats_pokemon_for(
            generation,
            type,
            include_legendaries,
            include_mythicals
        )

        return JsonResponse([
                PokemonStatsSerializer(pokemon_stat).data
                for pokemon_stat in pokemon_stats
            ],
            safe=False
        )
