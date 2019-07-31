"""lambdamud URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from django.contrib import admin
from mud.api import PlayerViewSet, PlayerInventoryViewSet, ItemViewSet, MapViewSet, RoomViewSet
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from mud.models import Player

router = routers.DefaultRouter()
router.register(r'player', PlayerViewSet)
router.register(r'playerinventory', PlayerInventoryViewSet)
router.register(r'item', ItemViewSet)
router.register(r'map', MapViewSet)
router.register(r'room', RoomViewSet)

# p = Player.objects.get(name='player87')
# p.go_to_room(1)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('player/<str:player>/go/<int:room>/', p.go_to_room),
    re_path(r'^api-token-auth/', views.obtain_auth_token)
]
