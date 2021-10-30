from rest_framework import viewsets

from coreAPI.models import Pokemon
from coreAPI.serializers import PokemonModelSerializer


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonModelSerializer
    permission_classes = []
    http_method_names = ['get']