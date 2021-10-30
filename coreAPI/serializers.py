from django.contrib.auth.models import User, Group
from rest_framework import serializers

from coreAPI.models import Pokemon


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PokemonModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonSerializer(serializers.Serializer):
    pokedex_number = serializers.IntegerField()
    name = serializers.CharField()
    generation = serializers.IntegerField()
    status = serializers.CharField()
    type_1 = serializers.CharField()
    type_2 = serializers.CharField()


class PokemonAbilitySerializer(serializers.Serializer):
    ability = serializers.CharField()

