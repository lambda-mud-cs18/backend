from django.db import models
from uuid import uuid4

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pass

class Team(model.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pass

class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    map_id = models.IntegerField() 
    pass

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
    east =  models.CharField(max_length=None)
    west =  models.CharField(max_length=None)