from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from coreAPI.models import PokemonStats, Pokemon
from coreAPI.serializers import PokemonStatsSerializer


class PokemonStatsAPI(APIView):
    def get(self, request):
        pokemon = get_object_or_404(Pokemon, id=self.request.GET.get('pokemon_id'))

        return JsonResponse(
            PokemonStatsSerializer(pokemon.stats).data,
            safe=False
        )


class BestPokemonAPIView(APIView):
    def get(self, request):
        generation = self.request.GET.get('generation')
        type = self.request.GET.get('type')
        include_legendaries = False if self.request.GET.get('include_legendaries') == 'False' else True
        include_mythicals = False if self.request.GET.get('include_mythicals') == 'False' else True
        include_mega_evolutions = False if self.request.GET.get('include_mega_evolutions') == 'False' else True

        pokemon_stats = PokemonStats.get_best_base_total_stats_pokemon_for(
            generation,
            type,
            include_legendaries,
            include_mythicals,
            include_mega_evolutions
        )

        return JsonResponse([
                PokemonStatsSerializer(pokemon_stat).data
                for pokemon_stat in pokemon_stats
            ],
            safe=False
        )
