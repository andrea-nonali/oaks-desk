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
    id = serializers.IntegerField()
    pokedex_number = serializers.IntegerField()
    name = serializers.CharField()
    generation = serializers.IntegerField()
    status = serializers.CharField()
    type_1 = serializers.CharField()
    type_2 = serializers.CharField()


class PokemonAbilitySerializer(serializers.Serializer):
    pokemon = serializers.CharField()
    ability_1 = serializers.CharField()
    ability_2 = serializers.CharField()
    ability_hidden = serializers.CharField()


class PokemonStatsSerializer(serializers.Serializer):
    pokemon = serializers.CharField()
    hp = serializers.IntegerField()
    attack = serializers.IntegerField()
    sp_attack = serializers.IntegerField()
    defense = serializers.IntegerField()
    sp_defense = serializers.IntegerField()
    speed = serializers.IntegerField()
    total_points = serializers.IntegerField()


