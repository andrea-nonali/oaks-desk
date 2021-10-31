from django.urls import path

from coreAPI.views.abilities_view import *
from coreAPI.views.pokemon_insights import *
from coreAPI.views.pokemon_stats_view import *
from coreAPI.views.type_intersections_view import *

urlpatterns = [
    path('get-abilities', PokemonAbilitiesAPI.as_view()),
    path('get-weak-against-pokemons', WeakAgainstAPI.as_view()),
    path('get-strong-against-pokemons', StrongAgainstAPI.as_view()),
    path('get-neutral-against-pokemons', NeutralAgainstAPI.as_view()),
    path('get-fully-covering-pokemons', CoveringPokemonsAPI.as_view()),
    path('get-stats', PokemonStatsAPI.as_view()),
    path('get-mega-evolutions', MegaEvolutionsAPI.as_view()),
    path('get-best_pokemons_stats', BestPokemonAPIView.as_view()),
]
