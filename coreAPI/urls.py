from django.urls import path

from coreAPI.views.abilities_view import PokemonAbilitiesAPI
from coreAPI.views.pokemon_insights import *
from coreAPI.views.stats_view import PokemonStatsAPIView
from coreAPI.views.type_intersections_view import WeakAgainstAPI, StrongAgainstAPI, NeutralAgainstAPI, \
    CoveringPokemonsAPI

urlpatterns = [
    path('get-abilities', PokemonAbilitiesAPI.as_view()),
    path('get-weak-against-pokemons', WeakAgainstAPI.as_view()),
    path('get-strong-against-pokemons', StrongAgainstAPI.as_view()),
    path('get-neutral-against-pokemons', NeutralAgainstAPI.as_view()),
    path('get-fully-covering-pokemons', CoveringPokemonsAPI.as_view()),
    path('get-stats', PokemonStatsAPIView.as_view()),
    path('get-mega-evolutions', MegaEvolutionsAPI.as_view()),
]
