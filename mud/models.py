from django.db import models
from uuid import uuid4
import requests

url = "https://lambda-treasure-hunt.herokuapp.com"
# token = 

# Create your models here.


class Player(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    playername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    team_id = models.IntegerField()
    # current room details
    current_room = models.IntegerField()
    cooldown = models.FloatField()
    encumbrance = models.IntegerField()
    strength = models.IntegerField()
    speed = models.IntegerField()
    gold = models.IntegerField()
    inventory = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    errors = models.CharField(max_length=1000)
    messages = models.CharField(max_length=1000)
    token = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def get_current_room(self):
        return self.current_room
    def travel(self, direction, next_room_id=None):
        # Function for the player to travel to the next room
        # Needs to be done after the cooldown
        pass
    def take(self):
        # Pickup the item in the current room
        # add the item to the player inventory
        # Needs to be done after the cooldown

        # If there arre multiple items in the room, pick them all up
        # for item in  res.items:
            # API call to TAKE
            # https://lambda-treasure-hunt.herokuapp.com/api/adv/take/
            # {
            #     "name":"{item}"
            # }
        pass
    def get_status(self):
        # https://lambda-treasure-hunt.herokuapp.com/api/adv/status/
        post_data = {}
        headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
        r = requests.post(url=url + "/api/adv/status/", json=post_data, headers=headers)
        data = r.json()
        print(data)
        if data.get('errors') is []:
            # To test out the function...
            # python3 manage.py shell
            # from mud.models import Player
            # p = Player.objects.get(name = 'player85')
            # p.get_status()

            # Update the player information in the DB
            Player.objects.filter(name = data.get('name')).update(name = data.get('name'),
                cooldown = data.get('cooldown'),
                encumbrance = data.get('encumbrance'),
                strength = data.get('strength'),
                speed = data.get('speed'),
                gold = data.get('gold'),
                inventory = data.get('inventory'),
                status = data.get('status'),
                errors = data.get('errors'),
                messages = data.get('messages'))
            
            # return data
        else:
            # There was an error
            Player.objects.filter(name = self.name).update(cooldown = data.get('cooldown'))
            print(data.get('cooldown'))


class PlayerInventory(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.AutoField(primary_key=True)

    player_id = models.IntegerField()
    item_id = models.IntegerField()
    quantity = models.IntegerField()


class Item(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    weight = models.IntegerField()
    itemtype = models.CharField(max_length=200)
    level = models.IntegerField()
    exp = models.IntegerField()
    attributes = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Team(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200)
    map_id = models.IntegerField()

    def __str__(self):
        return self.name


class Map(models.Model):
    id = models.AutoField(primary_key=True)
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # map_id = models.IntegerField()

    # def __str__(self):
    #     return self.map_id
    pass


class Room(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    map_id = models.IntegerField()
    room_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=200)
    elevation = models.IntegerField()
    terrain = models.CharField(max_length=200)
    north = models.CharField(max_length=200)
    south = models.CharField(max_length=200)
    east = models.CharField(max_length=200)
    west = models.CharField(max_length=200)

    def __str__(self):
        return self.room_id
    
    def getExits(self):
        exits = []
        if self.north is not None:
            exits.append("n")
        if self.south is not None:
            exits.append("s")
        if self.east is not None:
            exits.append("e")
        if self.west is not None:
            exits.append("w")
        return exits

