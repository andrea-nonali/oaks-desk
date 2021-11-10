from django.urls import include, path
from rest_framework import routers

import coreAPI.views.view_sets.group_view_set
import coreAPI.views.view_sets.pokemon_view_set
import coreAPI.views.view_sets.user_view_set
from coreAPI.views.pokemon_insights import *

router = routers.DefaultRouter()
router.register(r'users', coreAPI.views.view_sets.user_view_set.UserViewSet)
router.register(r'groups', coreAPI.views.view_sets.group_view_set.GroupViewSet)
router.register(r'pokemons', coreAPI.views.view_sets.pokemon_view_set.PokemonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('coreAPI.urls'))
]