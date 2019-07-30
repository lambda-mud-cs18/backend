# from rest_framework import serializers, viewsets
# from models import Player


# Describes which part of the model we want to expose to the API
# class Player(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Player
#         fields = ['playername', 'name', 'password', 'team_id', 'current_room',
#                   'cooldown', 'encumbrance', 'strength', 'speed', 'gold',
#                   'inventory', 'status', 'errors', 'messages', 'token']


# class PlayerViewSet(viewsets.ModelViewSet):
#     serializer_class = PersonalNoteSerializer
#     queryset = Player.objects.all()

from rest_framework import serializers, viewsets
from .models import Player

# convention is to name the serializer after what they are serializing


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    # inner class Meta describes what parts of the model we want to access

    class Meta:
        model = Player
        fields = ('playername', 'name', 'password', 'team_id', 'current_room',
                  'cooldown', 'encumbrance', 'strength', 'speed', 'gold',
                  'inventory', 'status', 'errors', 'messages', 'token')


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
