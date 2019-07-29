from django.db import models
from uuid import uuid4

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
