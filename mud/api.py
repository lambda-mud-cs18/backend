from rest_framework import serializers, viewsets
from .models import Player, PlayerInventory, Item, Team, Map, Room

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


class PlayerInventorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PlayerInventory
        fields = ('player_id', 'item_id', 'quantity')


class PlayerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerInventorySerializer
    queryset = PlayerInventory.objects.all()


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'description', 'weight',
                  'itemtype', 'level', 'exp', 'attributes')


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class MapSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Map
        fields = ()


class MapViewSet(viewsets.ModelViewSet):
    serializer_class = MapSerializer
    queryset = Map.objects.all()


class RoomSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Room
        fields = ('map_id', 'room_id', 'title', 'description', 'coordinates',
                  'elevation', 'terrain', 'north', 'south', 'east', 'west')


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
