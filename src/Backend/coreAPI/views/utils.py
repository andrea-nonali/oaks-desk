from django.http import Http404

from coreAPI.models import Pokemon


def get_pokemon(request):
    pokemon = Pokemon.get_pokemon_by_pokedex_number(request.GET.get('pokedex_number'))
    if not pokemon:
        return Http404()
    return pokemon