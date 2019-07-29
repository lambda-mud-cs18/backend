from django.contrib import admin
from .models import Player, PlayerInventory, Item, Team, Map, Room
# Register your models here.
admin.site.register(Player)
admin.site.register(PlayerInventory)
admin.site.register(Item)
admin.site.register(Team)
admin.site.register(Map)
admin.site.register(Room)
