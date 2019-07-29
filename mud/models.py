from django.db import models
from uuid import uuid4

# Create your models here.


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=None)
    name = models.CharField(max_length=None)
    password = models.CharField(max_length=None)
    team_id = model.IntegerField()
    # current room details
    current_room = models.IntegerField()
    cooldown = models.FloatField()
    encumbrance = models.IntegerField()
    strength = models.IntegerField()
    speed = models.IntegerField()
    gold = models.IntegerField()
    inventory = models.ArrayField(models.CharField(max_length=None), size=None)
    status = models.ArrayField(models.CharField(max_length=None), size=None)
    errors = models.ArrayField(models.CharField(max_length=None), size=None)
    messages = models.ArrayField(models.CharField(max_length=None), size=None)


class Team(model.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=None)
    map_id = models.IntegerField()


class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    map_id = models.IntegerField()


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    map_id = models.IntegerField()
    room_id = models.IntegerField()
    title = models.CharField(max_length=None)
    description = models.CharField(max_length=None)
    coordinates = models.CharField(max_length=None)
    elevation = models.IntegerField()
    terrain = models.CharField(max_length=None)
    north = models.CharField(max_length=None)
    south = models.CharField(max_length=None)
    east = models.CharField(max_length=None)
    west = models.CharField(max_length=None)
