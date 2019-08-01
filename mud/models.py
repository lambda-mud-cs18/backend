from django.db import models
from uuid import uuid4
import requests
import json
import time
import random
import hashlib

url = "https://lambda-treasure-hunt.herokuapp.com"


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    playername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    team_id = models.IntegerField()
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

    def sell_inventory(self):
        """
        Function to sell all of a players inventory
        """
        if self.current_room is 1:
            status = self.get_status()
            inventory = status.get('inventory')
            print("Items in inventory: ", inventory)
            time.sleep(self.cooldown)
            if inventory is not None:
                for item in inventory:
                    post_data = {"name": item, "confirm": "yes"}
                    print("post_data", post_data)
                    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
                    r = requests.post(url=url + "/api/adv/sell/", json=post_data, headers=headers)
                    data = r.json()

                    # print(data)
                    print(data.get('messages'))
                    self.cooldown = data.get('cooldown')
                    print("sell_inventory() ending cooling down for: ", self.cooldown, "seconds")
                    time.sleep(self.cooldown)
            else:
                print("you have nothing in your inventory")
        else:
            print("you need to be in room 1 to sell stuff")
            return

    def take(self):
        """
        Function to pickup every item in the current room
        """
        print("** take() function")
        room = self.init()
        items = room.get('items')
        print("Grabbing items: ", items)
        print("take() cooling down after init() for: ", self.cooldown, "seconds")
        time.sleep(self.cooldown)
        if items is not None:
            # If there are multiple items in the room, pick them all up
            for item in items:
                # API call to TAKE
                # https://lambda-treasure-hunt.herokuapp.com/api/adv/take/
                # { "name":"{item}" }

                post_data = {"name": item}
                # print("post_data", post_data)
                headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
                r = requests.post(url=url + "/api/adv/take/", json=post_data, headers=headers)
                data = r.json()

                self.cooldown = data.get('cooldown')
                print("Grab: ", item, "and cooling down for: ", self.cooldown, "seconds")
                time.sleep(self.cooldown)

    def get_status(self):
        """
        Function to get the player status
        https://lambda-treasure-hunt.herokuapp.com/api/adv/status/
        """
        print("** get_status() function")
        post_data = {}
        headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
        r = requests.post(url=url + "/api/adv/status/", json=post_data, headers=headers)
        data = r.json()
        if len(data.get('errors')) is 0:
            # To test out the function...
            # python3 manage.py shell
            # from mud.models import Player
            # p = Player.objects.get(name = 'brooks')
            # p.get_status()

            self.name = data.get('name')
            self.cooldown = data.get('cooldown')
            self.encumbrance = data.get('encumbrance')
            self.strength = data.get('strength')
            self.speed = data.get('speed')
            self.gold = data.get('gold')
            self.inventory = data.get('inventory')
            self.status = data.get('status')
            self.errors = data.get('errors')
            self.messages = data.get('messages')
            return data

        else:
            # There was an error
            self.cooldown = data.get('cooldown')
            print("get_status error: ", data)
            print("get_status() error: cool down for: ", data.get('cooldown'))
            time.sleep(self.cooldown)
            return data

    def init(self):
        """
        Function to get the player info
        https://lambda-treasure-hunt.herokuapp.com/api/adv/init/
        """
        print("** init() function")
        post_data = {}
        headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
        r = requests.get(url=url + "/api/adv/init/", json=post_data, headers=headers)
        data = r.json()
        if len(data.get('errors')) is 0:
            # To test out the function...
            # python3 manage.py shell
            # from mud.models import Player, Room
            # p = Player.objects.get(name = 'player85')
            # p.init()

            self.current_room = data.get('room_id')
            self.cooldown = data.get('cooldown')
            self.errors = data.get('errors')
            self.messages = data.get('messages')
            time.sleep(self.cooldown)
            return data
        else:
            # There was an error
            print("init() error: ", data)
            self.cooldown = data.get('cooldown')
            print("cool down for: ", self.cooldown)
            time.sleep(self.cooldown)
            return data

    def move(self, direction):
        """
        Function to move a player a single space
        Takes: direction
        https://lambda-treasure-hunt.herokuapp.com/api/adv/move/

        from mud.models import Player, Room
        p = Player.objects.get(name = 'brooks')
        p.move("s")
        """
        print("** move() function")
        self.get_status()
        print("move() sleeping after get_status() for: ",  self.cooldown)
        time.sleep(self.cooldown)
        print("current room: ", self.current_room, "direction: ", direction)
        next_room_id = Room().next_room(self.current_room, direction)
        print("next_room_id", next_room_id)
        fly_or_move = "/api/adv/move/"

        # Function to choose if we fly to the next room or move
        # We cannot fly when heavly encumbered
        if self.encumbrance <= 10:
            # We need to get the room infor for the next room from our DB
            r = requests.get(url="https://lambda-mud-18.herokuapp.com/api/room/?format=json")
            explored = r.json()
            for i in range(len(explored)):
                if int(explored[i].get('room_id')) == int(next_room_id):
                    # We need to see if the elevation for the next room is > 0
                    # If so, then we need to fly not move
                    if explored[i].get('elevation') > 0:
                        print("elevation: ", explored[i].get('elevation'))
                        fly_or_move = "/api/adv/fly/"

        print("fly_or_move", fly_or_move)

        # if next_room_id is not None:
        post_data = {
            "direction": direction,
            "next_room_id": next_room_id
        }
        # else:
        #     print("No room in that direction")
        #     return

        headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
        r = requests.post(url=url + fly_or_move, json=post_data, headers=headers)
        data = r.json()
        print("data", data)

        if len(data.get('errors')) is 0:
            # To test out the function...
            # python3 manage.py shell
            # from mud.models import Player, Room
            # p = Player.objects.get(name = 'brooks')
            # p.move("e")

            self.current_room = data.get('room_id')
            self.cooldown = data.get('cooldown')
            self.errors = data.get('errors')
            self.messages = data.get('messages')
            self.room_to_db(data.get('room_id'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'))

            return data

        else:
            # There was an error
            self.cooldown = data.get('cooldown')
            return data


    def explore(self, length):
        """
        Randomly explore the island the number of turns passed in
        """
        print("** explore() function")
        self.get_status()
        print("explore() cooling down after first get_status() for: ", self.cooldown, "seconds")
        time.sleep(self.cooldown)

        init = self.init()
        self.cooldown = init.get('cooldown')
        print("explore() cooling down after init() for: ", self.cooldown, "seconds")
        time.sleep(self.cooldown)
        exits = init.get('exits')

        i = 0
        while i < length:
            # look if encumbered
            status = self.get_status()
            encumbrance = status.get('encumbrance')
            print("explore() cooling down after second get_status() for: ", self.cooldown, "seconds")
            time.sleep(status.get('cooldown'))
            if encumbrance >= 9:
                print("/n/nEncumbered, going to sell inventory")
                # save current room
                saved_room = self.current_room
                # go to shop
                self.go_to_room(1)
                # sell_inventory
                print("Selling inventory")
                self.sell_inventory()
                # go back to the current room and keep exploring
                print("/n/nNow going back to original room: ", saved_room)
                self.go_to_room(saved_room)

            #  Take a random path
            random_exit = random.sample(exits, 1)
            print("random_exit", random_exit[0])

            move = self.move(random_exit[0])
            print("move: ", move)
            exits = move.get('exits')
            items = move.get('items')
            players = move.get('players')
            items = move.get('items')
            messages = move.get('messages')
            # self.room_to_db( move.get('room_id'), move.get('title'), move.get('description'), move.get('coordinates'), move.get('elevation'), move.get('terrain') )
            # If there are items, GET EM!
            if len(items) > 0:
                print("\n****************  ITEMS  *************")
                print("there be items here: ", items)
                print("\n**************************************")
                print("explore() cooling down before take() for: ", self.cooldown, "seconds")
                time.sleep(self.cooldown)
                self.take()

            # Tell me all the people in the room
            if len(players) > 0:
                print("\nthere be other players here")
                for person in players:
                    print("person:", person)
                    if person is "Pirate Ry":
                        print("****************PIRATE*************")
                        return move
            # Temm me any important messages
            if len(messages) > 2:
                print("\n*********IMPORTANT MESSAGES************")
                print(messages)
                print("\n**************************************")

            print("explore() last cooling down for: ", move.get('cooldown'), "seconds")
            time.sleep(self.cooldown)
            i += 1

    def go_to_room(self, room):
        """
        Function to go to a specific room.
        Will stop and pick up treasure along the way.
        Will print a list of peole in each room and any important messages.
        Takes: Destination room
        
        from mud.models import Player, Room
        p = Player.objects.get(name = 'brooks')
        p = Player.objects.get(name = 'Rory')
        p = Player.objects.get(name = 'JaRule')
        p.go_to_room(1)
        """
        print("** go_to_room(): ", room)
        self.get_status()
        print("go_to_room() cooling down after get_status() for: ", self.cooldown, "seconds")
        time.sleep(self.cooldown)

        self.init()
        print("go_to_room() cooling down after init() for: ", self.cooldown, "seconds")
        time.sleep(self.cooldown)
        # Perform bfs to find the shortest path to the given room
        path = self.bfs(room)
        print("path: ", path)

        # Travel along the "path" until we get to the destination
        for i in range(len(path)-1):
            current_room = path[i]
            next_room = path[i+1]

            # Look at the exits of the current room, go if the exit is the next room on the path
            for exits in island_map[str(current_room)][1]:
                if island_map[str(current_room)][1][exits] is next_room:
                    print("\nTRAVELING:", exits)
                    move = self.move(exits)
                    self.cooldown = move.get('cooldown')
                    print("go_to_room() cooling down after move() for: ", move.get('cooldown'), "seconds")
                    time.sleep(self.cooldown)
                    print(move)
                    items = move.get('items')
                    players = move.get('players')
                    messages = move.get('messages')
                    # print("move.get('room_id'), move.get('title'), move.get('description'), move.get('coordinates'), move.get('elevation'), move.get('terrain')", move.get('room_id'), move.get('title'), move.get('description'), move.get('coordinates'), move.get('elevation'), move.get('terrain'))
                    # self.room_to_db(move.get('room_id'), move.get('title'), move.get('description'), move.get('coordinates'), move.get('elevation'), move.get('terrain') )
                    
                    # If there are items, GET EM!
                    if len(items) > 0:
                        print("\n****************  ITEMS  *************")
                        print("there be items here: ", items)
                        print("\n**************************************")
                        print("go_to_room() cooling down before take() for: ", self.cooldown, "seconds")
                        time.sleep(self.cooldown)
                        self.take()

                    # Tell me all the people in the room
                    if len(players) > 0:
                        print("\nthere be other players here")
                        for person in players:
                            print("person:", person)

                    # Tell me any important messages
                    if len(messages) > 2:
                        print("\n*********IMPORTANT MESSAGES************")
                        print(messages)
                        print("\n***************************************")

                    # print("go_to_room() cooling down for: ", move.get('cooldown'), "seconds")
                    # time.sleep(self.cooldown)

        return f"Now in room: {self.current_room}"

    def bfs(self, destination):
        # print("** bfs()")
        # self.init()
        # print("bfs() cooling down after init() for: ", self.cooldown, "seconds")
        # time.sleep(self.cooldown)

        visited = set()
        q = []
        q.append([self.current_room])
        while len(q) > 0:
            v = q.pop()

            if v[-1] == destination:
                q = []  # Reset the Queue for next time
                return v

            elif v[-1] not in visited:
                visited.add(v[-1])
                for neighbor in island_map[str(v[-1])][1].values():
                    path = v.copy()
                    path.append(neighbor)
                    q.append(path)

    def pray(self):
        """
        Function to pray at a shrine
        https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/
        """
        print("Praying")
        post_data = {}
        headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
        r = requests.post(url=url + "/api/adv/pray/", json=post_data, headers=headers)
        data = r.json()
        print(data)

    def room_to_db(self, room_id, title, description, coordinates, elevation, terrain):
        print("** room_to_db()")
        north = Room().next_room(room_id, 'n')
        south = Room().next_room(room_id, 's')
        east = Room().next_room(room_id, 'e')
        west = Room().next_room(room_id, 'w')

        post_data = {
            "map_id": 1,
            "room_id": room_id,
            "title": title,
            "description": description,
            "coordinates": coordinates,
            "elevation": elevation,
            "terrain": terrain,
            "north": str(north),
            "south": str(south),
            "east": str(east),
            "west": str(west)
        }

        headers = {'content-type': 'application/json', 'Authorization': 'Token 982a27a7b299236b8aa9ee94ea7fa2458d64b2ee'}
        r = requests.post(url="https://lambda-mud-18.herokuapp.com/api/room/", json=post_data, headers=headers)
        data = r.json()

        room_id = data.get('room_id')
        if room_id == ['room with this room id already exists.']:
            pass
        else:
            print("New room added to DB: ", data)
    
    def unexplored(self):
        """
        Function to explore the unexplored parts of the map

        from mud.models import Player, Room
        p = Player.objects.get(name = 'brooks')
        p.unexplored()
        """
        print("\n** unexplored()")
        self.get_status()
        print("unexplored() cooling down after get_status() for: ", self.cooldown, "seconds")
        time.sleep(self.cooldown)

        r = requests.get(url="https://lambda-mud-18.herokuapp.com/api/room/?format=json")
        explored = r.json()
        # Make a list of all the rooms from the server that we have explored
        explored_list = []
        for i in range(len(explored)):
            explored_list.append(explored[i].get('room_id'))

        # Remove the explored rooms from a list of all rooms
        unexplored_list = list(range(500))
        for j in explored_list:
            # print("j", j)
            unexplored_list.remove(j)

        # Do BFS on all rooms and give me the shortest_path
        shortest_path = [0]*500
        for k in unexplored_list:
            new_path = self.bfs(k)

            if len(new_path) < len(shortest_path):
                shortest_path = new_path

        # Keep going to all the unexplored rooms
        while len(unexplored_list) > 0:
            # Perform a search for the closest unexplored room
            print("\nNext room:", shortest_path[-1])

            # Go to that room
            self.go_to_room(shortest_path[-1])
            print("\n\n Made it to room: ", shortest_path[-1])
            unexplored_list.remove(shortest_path[-1])
            print("List of unexplored rooms: ", unexplored_list)

    def proof_of_work(self, last_proof, difficulty):
        """
        Simple Proof of Work Algorithm
        """

        print("Searching for next proof")
        proof = 0
        while self.valid_proof(last_proof, proof, difficulty) is False:
            proof += 1

        print("Proof found: " + str(proof))
        return proof

    def valid_proof(self, last_proof, proof, difficulty):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 6
        leading zeroes?
        hashlib.sha256(guess).hexdigest()
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        listofzeros = [0] * difficulty
        listofzeros = ''.join(str(e) for e in listofzeros)
        # print("guess_hash[:difficulty]", guess_hash[:difficulty])
        # print("listofzeros", listofzeros)

        return guess_hash[:difficulty] == listofzeros

    def mine(self):
        # from mud.models import Player, Room
        # p = Player.objects.get(name = 'brooks')
        # p.mine()
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
        while True:
            
            # Get the last proof from the server
            headers = {'content-type': 'application/json', 'Authorization': 'Token ' + self.token}
            r = requests.get(url=node + "/last_proof", headers=headers)
            data = r.json()
            print(data)

            new_proof = self.proof_of_work(data.get('proof'), data.get('difficulty'))

            post_data = {"proof": new_proof}
            r = requests.post(url=node + "/mine/", json=post_data, headers=headers)
            data = r.json()
            self.cooldown = data.get('cooldown')
            if data.get('message') == 'New Block Forged':
                print("Mine that LambdaCoin!")
                print(data)
                print("mine() cooling down: ", self.cooldown, "seconds")
                time.sleep(self.cooldown)
            else:
                print(data)
                print("mine() cooling down: ", self.cooldown, "seconds")
                time.sleep(self.cooldown)


class PlayerInventory(models.Model):
    id = models.AutoField(primary_key=True)
    player_id = models.IntegerField()
    item_id = models.IntegerField()
    quantity = models.IntegerField()


class Item(models.Model):
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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    map_id = models.IntegerField()

    def __str__(self):
        return self.name


class Map(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Room(models.Model):
    # id = models.AutoField(primary_key=True)
    map_id = models.IntegerField()
    room_id = models.IntegerField(primary_key=True)
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
        return f"{self.room_id} - {self.title} - {self.description}"

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

    def next_room(self, current_room, direction):
        """
        This function will return what the next room is given the current room and a direction.
        Takes: current room, direction
        """
        # To test out the function...
        # python3 manage.py shell
        # from mud.models import Player, Room
        # Room().next_room(0, "w")

        try:
            next_room = island_map[str(current_room)][1][direction]
            return str(next_room)
        except KeyError:
            # print("room does not exist in that direction")
            return None


class PlayerMethods():

    def player_to_room(self, player, room):
        p = Player.objects.get(name=player)
        p.go_to_room(room)

    def player_unexplored(self, player):
        p = Player.objects.get(name=player)
        p.unexplored()

    def player_explore(self, player, length):
        p = Player.objects.get(name=player)
        p.explore(length)

island_map = {
    "0": [{"x": 60, "y": 60 }, { "n": 10, "s": 2, "e": 4, "w": 1 }],
    "1": [{"x": 59, "y": 60 }, { "e": 0 }],
    "2": [{"x": 60, "y": 59 }, { "n": 0, "s": 6, "e": 3 }],
    "3": [{"x": 61, "y": 59 }, { "s": 9, "e": 5, "w": 2 }],
    "4": [{"x": 61, "y": 60 }, { "n": 23, "e": 13, "w": 0 }],
    "5": [{"x": 62, "y": 59 }, { "w": 3 }],
    "6": [{"x": 60, "y": 58 }, { "n": 2, "w": 7 }],
    "7": [{"x": 59, "y": 58 }, { "n": 8, "e": 6, "w": 56 }],
    "8": [{"x": 59, "y": 59 }, { "s": 7, "w": 16 }],
    "9": [{"x": 61, "y": 58 }, { "n": 3, "s": 12, "e": 11 }],
    "10": [{"x": 60, "y": 61 }, { "n": 19, "s": 0, "w": 43 }],
    "11": [{"x": 62, "y": 58 }, { "e": 17, "w": 9 }],
    "12": [{"x": 61, "y": 57 }, { "n": 9, "s": 18, "e": 14, "w": 21 }],
    "13": [{"x": 62, "y": 60 }, { "e": 15, "w": 4 }],
    "14": [{"x": 62, "y": 57 }, { "s": 34, "e": 37, "w": 12 }],
    "15": [{"x": 63, "y": 60 }, { "w": 13 }],
    "16": [{"x": 58, "y": 59 }, { "n": 58, "e": 8, "w": 67 }],
    "17": [{"x": 63, "y": 58 }, { "n": 24, "e": 42, "w": 11 }],
    "18": [{"x": 61, "y": 56 }, { "n": 12, "s": 22, "w": 25 }],
    "19": [{"x": 60, "y": 62 }, { "n": 20, "s": 10, "w": 77 }],
    "20": [{"x": 60, "y": 63 }, { "n": 63, "s": 19, "e": 27, "w": 46 }],
    "21": [{"x": 60, "y": 57 }, { "e": 12, "w": 29 }],
    "22": [{"x": 61, "y": 55 }, { "n": 18, "s": 78, "w": 36 }],
    "23": [{"x": 61, "y": 61 }, { "s": 4, "e": 26 }],
    "24": [{"x": 63, "y": 59 }, { "s": 17 }],
    "25": [{"x": 60, "y": 56 }, { "e": 18 }],
    "26": [{"x": 62, "y": 61 }, { "e": 55, "w": 23 }],
    "27": [{"x": 61, "y": 63 }, { "n": 40, "s": 28, "e": 30, "w": 20 }],
    "28": [{"x": 61, "y": 62 }, { "n": 27 }],
    "29": [{"x": 59, "y": 57 }, { "s": 45, "e": 21, "w": 49 }],
    "30": [{"x": 62, "y": 63 }, { "s": 31, "e": 32, "w": 27 }],
    "31": [{"x": 62, "y": 62 }, { "n": 30, "e": 33 }],
    "32": [{"x": 63, "y": 63 }, { "n": 39, "e": 54, "w": 30 }],
    "33": [{"x": 63, "y": 62 }, { "e": 38, "w": 31 }],
    "34": [{"x": 62, "y": 56 }, { "n": 14, "s": 50, "e": 35 }],
    "35": [{"x": 63, "y": 56 }, { "s": 52, "w": 34 }],
    "36": [{"x": 60, "y": 55 }, { "s": 48, "e": 22, "w": 60 }],
    "37": [{"x": 63, "y": 57 }, { "w": 14 }],
    "38": [{"x": 64, "y": 62 }, { "s": 59, "e": 66, "w": 33 }],
    "39": [{"x": 63, "y": 64 }, { "n": 53, "s": 32, "e": 51, "w": 41 }],
    "40": [{"x": 61, "y": 64 }, { "s": 27 }],
    "41": [{"x": 62, "y": 64 }, { "e": 39 }],
    "42": [{"x": 64, "y": 58 }, { "n": 44, "s": 80, "e": 118, "w": 17 }],
    "43": [{"x": 59, "y": 61 }, { "e": 10, "w": 47 }],
    "44": [{"x": 64, "y": 59 }, { "s": 42 }],
    "45": [{"x": 59, "y": 56 }, { "n": 29, "s": 60 }],
    "46": [{"x": 59, "y": 63 }, { "e": 20, "w": 62 }],
    "47": [{"x": 58, "y": 61 }, { "n": 71, "e": 43 }],
    "48": [{"x": 60, "y": 54 }, { "n": 36, "s": 105, "w": 149 }],
    "49": [{"x": 58, "y": 57 }, { "s": 79, "e": 29, "w": 136 }],
    "50": [{"x": 62, "y": 55 }, { "n": 34, "s": 89 }],
    "51": [{"x": 64, "y": 64 }, { "n": 69, "e": 57, "w": 39 }],
    "52": [{ "x": 63, "y": 55 }, { "n": 35, "s": 68, "e": 75 }],
    "53": [{ "x": 63, "y": 65 }, { "n": 95, "s": 39, "w": 88 }],
    "54": [{ "x": 64, "y": 63 }, { "w": 32 }],
    "55": [{ "x": 63, "y": 61 }, { "w": 26 }],
    "56": [{ "x": 58, "y": 58 }, { "e": 7, "w": 61 }],
    "57": [{ "x": 65, "y": 64 }, { "e": 145, "w": 51 }],
    "58": [{ "x": 58, "y": 60 }, { "s": 16, "w": 65 }],
    "59": [{ "x": 64, "y": 61 }, { "n": 38, "s": 104, "e": 92 }],
    "60": [{ "x": 59, "y": 55 }, { "n": 45, "e":36 ,"w": 70 }],
    "61": [{ "x": 57, "y": 58 }, { "e": 56, "w": 171 }],
    "62": [{ "x": 58, "y": 63 }, { "n": 64, "e": 46, "w": 84 }],
    "63": [{ "x": 60, "y": 64 }, { "n": 72, "s": 20, "w": 73 }],
    "64": [{ "x": 58, "y": 64 }, { "s": 62, "w": 82 }],
    "65": [{ "x": 57, "y": 60 }, { "n": 74, "e": 58, "w": 139 }],
    "66": [{ "x": 65, "y": 62 }, { "n": 169, "e": 123, "w": 38 }],
    "67": [{ "x": 57, "y": 59 }, { "e": 16, "w": 162 }],
    "68": [{ "x": 63, "y": 54 }, { "n": 52, "e": 100 }],
    "69": [{ "x": 64, "y": 65 }, { "n": 94, "s": 51, "e": 103 }],
    "70": [{ "x": 58, "y": 55 }, { "s": 163, "e": 60, "w": 98 }],
    "71": [{ "x": 58, "y": 62 }, { "s": 47 }],
    "72": [{ "x": 60, "y": 65 }, { "s": 63, "w": 76 }],
    "73": [{ "x": 59, "y": 64 }, { "e": 63 }],
    "74": [{ "x": 57, "y": 61 }, { "n": 87, "s": 65, "w": 161 }],
    "75": [{ "x": 64, "y": 55 }, { "e": 85, "w": 52 }],
    "76": [{ "x": 59, "y": 65 }, { "n": 83, "e": 72, "w": 110 }],
    "77": [{ "x": 59, "y": 62 }, { "e": 19 }],
    "78": [{ "x": 61, "y": 54 }, { "n": 22, "s": 108 }],
    "79": [{ "x": 58, "y": 56 }, { "n": 49 }],
    "80": [{ "x": 64, "y": 57 }, { "n": 42, "s": 81, "e": 86 }],
    "81": [{ "x": 64, "y": 56 }, { "n": 80 }],
    "82": [{ "x": 57, "y": 64 }, { "n": 191, "e": 64 }],
    "83": [{ "x": 59, "y": 66 }, { "s": 76, "e": 130, "w": 125 }],
    "84": [{ "x": 57, "y": 63 }, { "e": 62, "w": 91 }],
    "85": [{ "x": 65, "y": 55 }, { "e": 154, "w": 75 }],
    "86": [{ "x": 65, "y": 57 }, { "s": 96, "e": 90, "w": 80 }],
    "87": [{ "x": 57, "y": 62 }, { "s": 74 }],
    "88": [{ "x": 62, "y": 65 }, { "e": 53, "w": 122 }],
    "89": [{ "x": 62, "y": 54 }, { "n": 50, "s": 93 }],
    "90": [{ "x": 66, "y": 57 }, { "e": 178, "w": 86 }],
    "91": [{ "x": 56, "y": 63 }, { "n": 180, "s": 101, "e": 84, "w": 99 }],
    "92": [{ "x": 65, "y": 61 }, { "w": 59 }],
    "93": [{ "x": 62, "y": 53 }, { "n": 89, "w": 108}],
    "94": [{ "x": 64, "y": 66 }, { "n": 152, "s": 69 }],
    "95": [{ "x": 63, "y": 66 }, { "n": 119, "s": 53, "w": 115 }],
    "96": [{ "x": 65, "y": 56 }, { "n": 86, "e": 97 }],
    "97": [{ "x": 66, "y": 56 }, { "e": 181, "w": 96 }],
    "98": [{ "x": 57, "y": 55 }, { "n": 102, "s": 126, "e": 70, "w": 109 }],
    "99": [{ "x": 55, "y": 63 }, { "n": 190, "e": 91, "w": 146 }],
    "100": [{ "x": 64, "y": 54 }, { "s": 106, "e": 112, "w": 68 }],
    "101": [{ "x": 56, "y": 62 }, { "n": 91, "w": 113 }],
    "102": [{ "x": 57, "y": 56 }, { "s": 98, "w": 142 }],
    "103": [{ "x": 65, "y": 65 }, { "n": 160, "w": 69 }],
    "104": [{ "x": 64, "y": 60 }, { "n": 59, "e": 107 }],
    "105": [{ "x": 60, "y": 53 }, { "n": 48, "w": 202 }],
    "106": [{ "x": 64, "y": 53 }, { "n": 100, "s": 111, "w": 135 }],
    "107": [{ "x": 65, "y": 60 }, { "s": 120, "e": 121, "w": 104 }],
    "108": [{ "x": 61, "y": 53 }, { "n": 78, "s": 117 }],
    "109": [{ "x": 56, "y": 55 }, { "s": 185, "e": 98, "w": 175 }],
    "110": [{ "x": 58, "y": 65 }, { "e": 76 }],
    "111": [{ "x": 64, "y": 52 }, { "n": 106, "s": 367, "e": 158 }],
    "112": [{ "x": 65, "y": 54 }, { "s": 141, "e": 140, "w": 100 }],
    "113": [{ "x": 55, "y": 62 }, { "s": 114, "e": 101 }],
    "114": [{ "x": 55, "y": 61 }, { "n": 113, "w": 176 }],
    "115": [{ "x": 62, "y": 66 }, { "n": 116, "e": 95 }],
    "116": [{ "x": 62, "y": 67 }, { "n": 132, "s": 115 }],
    "117": [{ "x": 61, "y": 52 }, { "n": 108, "s": 131, "w": 133 }],
    "118": [{ "x": 65, "y": 58 }, { "e": 137, "w": 42 }],
    "119": [{ "x": 63, "y": 67 }, { "n": 134, "s": 95 }],
    "120": [{ "x": 65, "y": 59 }, { "n": 107, "e": 127 }],
    "121": [{ "x": 66, "y": 60 }, { "n": 128, "e": 143, "w": 107 }],
    "122": [{ "x": 61, "y": 65 }, { "n": 124, "e": 88 }],
    "123": [{ "x": 66, "y": 62 }, { "w": 66 }],
    "124": [{ "x": 61, "y": 66 }, { "n": 157, "s": 122 }],
    "125": [{ "x": 58, "y": 66 }, { "n": 165, "e": 83, "w": 237 }],
    "126": [{ "x": 57, "y": 54 }, { "n": 98, "s": 129 }],
    "127": [{ "x": 66, "y": 59 }, { "e": 184, "w": 120 }],
    "128": [{ "x": 66, "y": 61 }, { "s": 121, "e": 189 }],
    "129": [{ "x": 57, "y": 53 }, { "n": 126, "e": 194, "w": 170 }],
    "130": [{ "x": 60, "y": 66 }, { "w": 83 }],
    "131": [{ "x": 61, "y": 51 }, { "n": 117, "w": 138 }],
    "132": [{ "x": 62, "y": 68 }, { "s": 116 }],
    "133": [{ "x": 60, "y": 52 }, { "e": 117, "w": 173 }],
    "134": [{ "x": 63, "y": 68 }, { "n": 147, "s": 119, "e": 144 }],
    "135": [{ "x": 63, "y": 53 }, { "s": 150, "e": 106 }],
    "136": [{ "x": 57, "y": 57 }, { "e": 49, "w": 148 }],
    "137": [{ "x": 66, "y": 58 }, { "w": 118 }],
    "138": [{ "x": 60, "y": 51 }, { "s": 211, "e": 131, "w": 195 }],
    "139": [{ "x": 56, "y": 60 }, { "e": 65, "w": 188 }],
    "140": [{ "x": 66, "y": 54 }, { "w": 112 }],
    "141": [{ "x": 65, "y": 53 }, { "n": 112, "e": 156 }],
    "142": [{ "x": 56, "y": 56 }, { "e": 102, "w": 159 }],
    "143": [{ "x": 67, "y": 60 }, { "e": 212, "w": 121 }],
    "144": [{ "x": 64, "y": 68 }, { "e": 155, "w": 134 }],
    "145": [{ "x": 66, "y": 64 }, { "n": 174, "e": 220, "w": 57 }],
    "146": [{ "x": 54, "y": 63 }, { "n": 215, "s": 177, "e": 99, "w": 257 }],
    "147": [{ "x": 63, "y": 69 }, { "n": 200, "s": 134, "e": 153, "w": 151 }],
    "148": [{ "x": 56, "y": 57 }, { "e": 136, "w": 292 }],
    "149": [{ "x": 59, "y": 54 }, { "e": 48 }],
    "150": [{ "x": 63, "y": 52 }, { "n": 135, "w": 166 }],
    "151": [{ "x": 62, "y": 69 }, { "n": 172, "e": 147, "w": 207 }],
    "152": [{ "x": 64, "y": 67 }, { "s": 94 }],
    "153": [{ "x": 64, "y": 69 }, { "e": 329, "w": 147 }],
    "154": [{ "x": 66, "y": 55 }, { "e": 193, "w": 85 }],
    "155": [{ "x": 65, "y": 68 }, { "s": 187, "e": 316, "w": 144 }],
    "156": [{ "x": 66, "y": 53 }, { "s": 168, "e": 164, "w": 141 }],
    "157": [{ "x": 61, "y": 67 }, { "n": 210, "s": 124, "w": 182 }],
    "158": [{ "x": 65, "y": 52 }, { "s": 167, "w": 111 }],
    "159": [{ "x": 55, "y": 56 }, { "e": 142, "w": 196 }],
    "160": [{ "x": 65, "y": 66 }, { "s": 103 }],
    "161": [{ "x": 56, "y": 61 }, { "e": 74 }],
    "162": [{ "x": 56, "y": 59 }, { "e": 67 }],
    "163": [{ "x": 58, "y": 54 }, { "n": 70 }],
    "164": [{ "x": 67, "y": 53 }, { "n": 217, "e": 298, "w": 156 }],
    "165": [{ "x": 58, "y": 67 }, { "n": 203, "s": 125, "w": 204 }],
    "166": [{ "x": 62, "y": 52 }, { "s": 198, "e": 150 }],
    "167": [{ "x": 65, "y": 51 }, { "n": 158, "s": 262, "e": 260 }],
    "168": [{ "x": 66, "y": 52 }, { "n": 156, "e": 340 }],
    "169": [{ "x": 65, "y": 63 }, { "s": 66, "e": 186 }],
    "170": [{ "x": 56, "y": 53 }, { "e": 129 }],
    "171": [{ "x": 56, "y": 58 }, { "e": 61 }],
    "172": [{ "x": 62, "y": 70 }, { "n": 267, "s": 151 }],
    "173": [{ "x": 59, "y": 52 }, { "e": 133 }],
    "174": [{ "x": 66, "y": 65 }, { "n": 192, "s": 145, "e": 224 }],
    "175": [{ "x": 55, "y": 55 }, { "s": 183, "e": 109, "w": 179 }],
    "176": [{ "x": 54, "y": 61 }, { "e": 114, "w": 402 }],
    "177": [{ "x": 54, "y": 62 }, { "n": 146, "w": 346 }],
    "178": [{ "x": 67, "y": 57 }, { "n": 209, "e": 243, "w": 90 }],
    "179": [{ "x": 54, "y": 55 }, { "s": 233, "e": 175, "w": 213 }],
    "180": [{ "x": 56, "y": 64 }, { "s": 91 }],
    "181": [{ "x": 67, "y": 56 }, { "w": 97 }],
    "182": [{ "x": 60, "y": 67 }, { "e": 157, "w": 208 }],
    "183": [{ "x": 55, "y": 54 }, { "n": 175, "s": 229 }],
    "184": [{ "x": 67, "y": 59 }, { "e": 221, "w": 127 }],
    "185": [{ "x": 56, "y": 54 }, { "n": 109 }],
    "186": [{ "x": 66, "y": 63 }, { "e": 205, "w": 169 }],
    "187": [{ "x": 65, "y": 67 }, { "n": 155 }],
    "188": [{ "x": 55, "y": 60 }, { "e": 139, "w": 335 }],
    "189": [{ "x": 67, "y": 61 }, { "e": 255, "w": 128 }],
    "190": [{ "x": 55, "y": 64 }, { "s": 99 }],
    "191": [{ "x": 57, "y": 65 }, { "s": 82 }],
    "192": [{ "x": 66, "y": 66 }, { "n": 201, "s": 174, "e": 223 }],
    "193": [{ "x": 67, "y": 55 }, { "e": 251, "w": 154 }],
    "194": [{ "x": 58, "y": 53 }, { "s": 214, "w": 129 }],
    "195": [{ "x": 59, "y": 51 }, { "s": 228, "e": 138, "w": 225 }],
    "196": [{ "x": 54, "y": 56 }, { "n": 222, "e": 159, "w": 197 }],
    "197": [{ "x": 53, "y": 56 }, { "n": 232, "e": 196, "w": 276 }],
    "198": [{ "x": 62, "y": 51 }, { "n": 166, "s": 239, "e": 199 }],
    "199": [{ "x": 63, "y": 51 }, { "s": 230, "w": 198 }],
    "200": [{ "x": 63, "y": 70 }, { "n": 227, "s": 147, "e": 206 }],
    "201": [{ "x": 66, "y": 67 }, { "s": 192 }],
    "202": [{ "x": 59, "y": 53 }, { "e": 105 }],
    "203": [{ "x": 58, "y": 68 }, { "n": 268, "s": 165, "e": 299 }],
    "204": [{ "x": 57, "y": 67 }, { "n": 219, "e": 165, "w": 216 }],
    "205": [{ "x": 67, "y": 63 }, { "s": 241, "e": 479, "w": 186 }],
    "206": [{ "x": 64, "y": 70 }, { "n": 288, "e": 380, "w": 200 }],
    "207": [{ "x": 61, "y": 69 }, { "n": 231, "e": 151, "w": 290 }],
    "208": [{ "x": 59, "y": 67 }, { "e": 182 }],
    "209": [{ "x": 67, "y": 58 }, { "s": 178 }],
    "210": [{ "x": 61, "y": 68 }, { "s": 157 }],
    "211": [{ "x": 60, "y": 50 }, { "n": 138 }],
    "212": [{ "x": 68, "y": 60 }, { "w": 143 }],
    "213": [{ "x": 53, "y": 55 }, { "e": 179, "w": 420 }],
    "214": [{ "x": 58, "y": 52 }, { "n": 194, "w": 226 }],
    "215": [{ "x": 54, "y": 64 }, { "n": 246, "s": 146 }],
    "216": [{ "x": 56, "y": 67 }, { "n": 234, "e": 204, "w": 218 }],
    "217": [{ "x": 67, "y": 54 }, { "s": 164, "e": 247 }],
    "218": [{ "x": 55, "y": 67 }, { "s": 263, "e": 216, "w": 242 }],
    "219": [{ "x": 57, "y": 68 }, { "s": 204 }],
    "220": [{ "x": 67, "y": 64 }, { "w": 145 }],
    "221": [{ "x": 68, "y": 59 }, { "s": 253, "e": 240, "w": 184 }],
    "222": [{ "x": 54, "y": 57 }, { "n": 305, "s": 196 }],
    "223": [{ "x": 67, "y": 66 }, { "n": 283, "w": 192 }],
    "224": [{ "x": 67, "y": 65 }, { "w": 174 }],
    "225": [{ "x": 58, "y": 51 }, { "s": 278, "e": 195 }],
    "226": [{ "x": 57, "y": 52 }, { "s": 300, "e": 214 }],
    "227": [{ "x": 63, "y": 71 }, { "n": 269, "s": 200 }],
    "228": [{ "x": 59, "y": 50 }, { "n": 195, "s": 281 }],
    "229": [{ "x": 55, "y": 53 }, { "n": 183, "s": 250, "w": 236 }],
    "230": [{ "x": 63, "y": 50 }, { "n": 199, "s": 307, "e": 297 }],
    "231": [{ "x": 61, "y": 70 }, { "s": 207, "w": 248 }],
    "232": [{ "x": 53, "y": 57 }, { "n": 272, "s": 197, "w": 235 }],
    "233": [{ "x": 54, "y": 54 }, { "n": 179, "w": 238 }],
    "234": [{ "x": 56, "y": 68 }, { "n": 368, "s": 216, "w": 252 }],
    "235": [{ "x": 52, "y": 57 }, { "n": 330, "e": 232, "w": 355 }],
    "236": [{ "x": 54, "y": 53 }, { "s": 264, "e": 229 }],
    "237": [{ "x": 57, "y": 66 }, { "e": 125, "w": 245 }],
    "238": [{ "x": 53, "y": 54 }, { "e": 233 }],
    "239": [{ "x": 62, "y": 50 }, { "n": 198, "w": 244 }],
    "240": [{ "x": 69, "y": 59 }, { "n": 249, "e": 386, "w": 221 }],
    "241": [{ "x": 67, "y": 62 }, { "n": 205, "e": 266 }],
    "242": [{ "x": 54, "y": 67 }, { "n": 287, "s": 259, "e": 218, "w": 275 }],
    "243": [{ "x": 68, "y": 57 }, { "s": 293, "e": 256, "w": 178 }],
    "244": [{ "x": 61, "y": 50 }, { "e": 239 }],
    "245": [{ "x": 56, "y": 66 }, { "s": 254, "e": 237 }],
    "246": [{ "x": 54, "y": 65 }, { "s": 215 }],
    "247": [{ "x": 68, "y": 54 }, { "e": 261, "w": 217 }],
    "248": [{ "x": 60, "y": 70 }, { "n": 296, "e": 231, "w": 280 }],
    "249": [{ "x": 69, "y": 60 }, { "n": 265, "s": 240, "e": 282 }],
    "250": [{ "x": 55, "y": 52 }, { "n": 229, "s": 294, "e": 289 }],
    "251": [{ "x": 68, "y": 55 }, { "e": 315, "w": 193 }],
    "252": [{ "x": 55, "y": 68 }, { "n": 284, "e": 234 }],
    "253": [{ "x": 68, "y": 58 }, { "n": 221, "e": 258 }],
    "254": [{ "x": 56, "y": 65 }, { "n": 245, "w": 314 }],
    "255": [{ "x": 68, "y": 61 }, { "w": 189 }],
    "256": [{ "x": 69, "y": 57 }, { "s": 360, "e": 327, "w": 243 }],
    "257": [{ "x": 53, "y": 63 }, { "n": 320, "e": 146, "w": 364 }],
    "258": [{ "x": 69, "y": 58 }, { "e": 306, "w": 253 }],
    "259": [{ "x": 54, "y": 66 }, { "n": 242, "w": 310 }],
    "260": [{ "x": 66, "y": 51 }, { "w": 167 }],
    "261": [{ "x": 69, "y": 54 }, { "s": 277, "e": 322, "w": 247 }],
    "262": [{ "x": 65, "y": 50 }, { "n": 167, "s": 370, "e": 358 }],
    "263": [{ "x": 55, "y": 66 }, { "n": 218 }],
    "264": [{ "x": 54, "y": 52 }, { "n": 236, "s": 274, "w": 273 }],
    "265": [{ "x": 69, "y": 61 }, { "n": 279, "s": 249, "e": 270 }],
    "266": [{ "x": 68, "y": 62 }, { "w": 241 }],
    "267": [{ "x": 62, "y": 71 }, { "n": 285, "s": 172, "w": 271 }],
    "268": [{ "x": 58, "y": 69 }, { "s": 203, "e": 411, "w": 312 }],
    "269": [{ "x": 63, "y": 72 }, { "n": 319, "s": 227 }],
    "270": [{ "x": 70, "y": 61 }, { "n": 416, "e": 338, "w": 265 }],
    "271": [{ "x": 61, "y": 71 }, { "n": 337, "e": 267 }],
    "272": [{ "x": 53, "y": 58 }, { "n": 295, "s": 232 }],
    "273": [{ "x": 53, "y": 52 }, { "n": 343, "e": 264 }],
    "274": [{ "x": 54, "y": 51 }, { "n": 264, "w": 308 }],
    "275": [{ "x": 53, "y": 67 }, { "e": 242, "w": 456 }],
    "276": [{ "x": 52, "y": 56 }, { "e": 197, "w": 419 }],
    "277": [{ "x": 69, "y": 53 }, { "n": 261, "e": 323 }],
    "278": [{ "x": 58, "y": 50 }, { "n": 225 }],
    "279": [{ "x": 69, "y": 62 }, { "s": 265 }],
    "280": [{ "x": 59, "y": 70 }, { "n": 325, "e": 248 }],
    "281": [{ "x": 59, "y": 49 }, { "n": 228, "s": 318, "e": 309, "w": 317 }],
    "282": [{ "x": 70, "y": 60 }, { "w": 249 }],
    "283": [{ "x": 67, "y": 67 }, { "n": 331, "s": 223, "e": 313 }],
    "284": [{ "x": 55, "y": 69 }, { "n": 302, "s": 252, "w": 303 }],
    "285": [{ "x": 62, "y": 72 }, { "n": 286, "s": 267 }],
    "286": [{ "x": 62, "y": 73 }, { "n": 336, "s": 285, "w": 291 }],
    "287": [{ "x": 54, "y": 68 }, { "s": 242, "w": 339 }],
    "288": [{ "x": 64, "y": 71 }, { "s": 206 }],
    "289": [{ "x": 56, "y": 52 }, { "w": 250 }],
    "290": [{ "x": 60, "y": 69 }, { "e": 207 }],
    "291": [{ "x": 61, "y": 73 }, { "n": 410, "e": 286, "w": 347 }],
    "292": [{ "x": 55, "y": 57 }, { "n": 301, "e": 148 }],
    "293": [{ "x": 68, "y": 56 }, { "n": 243 }],
    "294": [{ "x": 55, "y": 51 }, { "n": 250, "s": 334 }],
    "295": [{ "x": 53, "y": 59 }, { "s": 272 }],
    "296": [{ "x": 60, "y": 71 }, { "s": 248 }],
    "297": [{ "x": 64, "y": 50 }, { "w": 230 }],
    "298": [{ "x": 68, "y": 53 }, { "s": 324, "w": 164 }],
    "299": [{ "x": 59, "y": 68 }, { "e": 311, "w": 203 }],
    "300": [{ "x": 57, "y": 51 }, { "n": 226, "s": 377, "w": 389 }],
    "301": [{ "x": 55, "y": 58 }, { "n": 304, "s": 292 }],
    "302": [{ "x": 55, "y": 70 }, { "n": 422, "s": 284 }],
    "303": [{ "x": 54, "y": 69 }, { "n": 361, "e": 284, "w": 405 }],
    "304": [{ "x": 55, "y": 59 }, { "s": 301 }],
    "305": [{ "x": 54, "y": 58 }, { "n": 365, "s": 222 }],
    "306": [{ "x": 70, "y": 58 }, { "e": 397, "w": 258 }],
    "307": [{ "x": 63, "y": 49 }, { "n": 230, "s": 373, "e": 371, "w": 321 }],
    "308": [{ "x": 53, "y": 51 }, { "e": 274 }],
    "309": [{ "x": 60, "y": 49 }, { "s": 333, "e": 326, "w": 281 }],
    "310": [{ "x": 53, "y": 66 }, { "e": 259, "w": 412 }],
    "311": [{ "x": 60, "y": 68 }, { "w": 299 }],
    "312": [{ "x": 57, "y": 69 }, { "n": 328, "e": 268 }],
    "313": [{ "x": 68, "y": 67 }, { "w": 283 }],
    "314": [{ "x": 55, "y": 65 }, { "e": 254 }],
    "315": [{ "x": 69, "y": 55 }, { "w": 251 }],
    "316": [{ "x": 66, "y": 68 }, { "n": 344, "w": 155 }],
    "317": [{ "x": 58, "y": 49 }, { "s": 387, "e": 281, "w": 409 }],
    "318": [{ "x": 59, "y": 48 }, { "n": 281, "s": 487 }],
    "319": [{ "x": 63, "y": 73 }, { "n": 359, "s": 269, "e": 345 }],
    "320": [{ "x": 53, "y": 64 }, { "n": 348, "s": 257 }],
    "321": [{ "x": 62, "y": 49 }, { "s": 413, "e": 307 }],
    "322": [{ "x": 70, "y": 54 }, { "n": 382, "e": 435, "w": 261 }],
    "323": [{ "x": 70, "y": 53 }, { "e": 433, "w": 277 }],
    "324": [{ "x": 68, "y": 52 }, { "n": 298, "s": 349, "e": 354 }],
    "325": [{ "x": 59, "y": 71 }, { "n": 353, "s": 280, "w": 374 }],
    "326": [{ "x": 61, "y": 49 }, { "s": 342, "w": 309 }],
    "327": [{ "x": 70, "y": 57 }, { "e": 427, "w": 256 }],
    "328": [{ "x": 57, "y": 70 }, { "n": 332, "s": 312, "e": 357, "w": 363 }],
    "329": [{ "x": 65, "y": 69 }, { "w": 153 }],
    "330": [{ "x": 52, "y": 58 }, { "n": 369, "s": 235, "w": 383 }],
    "331": [{ "x": 67, "y": 68 }, { "s": 283, "e": 446 }],
    "332": [{ "x": 57, "y": 71 }, { "n": 350, "s": 328 }],
    "333": [{ "x": 60, "y": 48 }, { "n": 309, "s": 378 }],
    "334": [{ "x": 55, "y": 50 }, { "n": 294, "s": 393, "e": 341, "w": 391 }],
    "335": [{ "x": 54, "y": 60 }, { "e": 188, "w": 366 }],
    "336": [{ "x": 62, "y": 74 }, { "s": 286 }],
    "337": [{ "x": 61, "y": 72 }, { "s": 271 }],
    "338": [{ "x": 71, "y": 61 }, { "s": 379, "w": 270 }],
    "339": [{ "x": 53, "y": 68 }, { "e": 287, "w": 445 }],
    "340": [{ "x": 67, "y": 52 }, { "w": 168 }],
    "341": [{ "x": 56, "y": 50 }, { "s": 449, "w": 334 }],
    "342": [{ "x": 61, "y": 48 }, { "n": 326, "s": 432 }],
    "343": [{ "x": 53, "y": 53 }, { "s": 273, "w": 351 }],
    "344": [{ "x": 66, "y": 69 }, { "n": 392, "s": 316, "e": 390 }],
    "345": [{ "x": 64, "y": 73 }, { "s": 375, "w": 319 }],
    "346": [{ "x": 53, "y": 62 }, { "e": 177 }],
    "347": [{ "x": 60, "y": 73 }, { "n": 452, "s": 442, "e": 291 }],
    "348": [{ "x": 53, "y": 65 }, { "s": 320 }],
    "349": [{ "x": 68, "y": 51 }, { "n": 324, "s": 352, "e": 384, "w": 356 }],
    "350": [{ "x": 57, "y": 72 }, { "n": 436, "s": 332, "e": 404 }],
    "351": [{ "x": 52, "y": 53 }, { "s": 491, "e": 343, "w": 478 }],
    "352": [{ "x": 68, "y": 50 }, { "n": 349, "s": 362, "e": 485 }],
    "353": [{ "x": 59, "y": 72 }, { "s": 325 }],
    "354": [{ "x": 69, "y": 52 }, { "w": 324 }],
    "355": [{ "x": 51, "y": 57 }, { "e": 235 }],
    "356": [{ "x": 67, "y": 51 }, { "e": 349 }],
    "357": [{ "x": 58, "y": 70 }, { "w": 328 }],
    "358": [{ "x": 66, "y": 50 }, { "e": 401, "w": 262 }],
    "359": [{ "x": 63, "y": 74 }, { "s": 319 }],
    "360": [{ "x": 69, "y": 56 }, { "n": 256, "e": 398 }],
    "361": [{ "x": 54, "y": 70 }, { "n": 408, "s": 303 }],
    "362": [{ "x": 68, "y": 49 }, { "n": 352, "s": 399, "w": 463 }],
    "363": [{ "x": 56, "y": 70 }, { "n": 372, "e": 328 }],
    "364": [{ "x": 52, "y": 63 }, { "n": 429, "s": 381, "e": 257, "w": 448 }],
    "365": [{ "x": 54, "y": 59 }, { "s": 305 }],
    "366": [{ "x": 53, "y": 60 }, { "e": 335 }],
    "367": [{ "x": 64, "y": 51 }, { "n": 111 }],
    "368": [{ "x": 56, "y": 69 }, { "s": 234 }],
    "369": [{ "x": 52, "y": 59 }, { "n": 400, "s": 330, "w": 376 }],
    "370": [{ "x": 65, "y": 49 }, { "n": 262, "s": 434, "e": 407 }],
    "371": [{ "x": 64, "y": 49 }, { "s": 475, "w": 307 }],
    "372": [{ "x": 56, "y": 71 }, { "n": 441, "s": 363 }],
    "373": [{ "x": 63, "y": 48 }, { "n": 307, "s": 480 }],
    "374": [{ "x": 58, "y": 71 }, { "e": 325 }],
    "375": [{ "x": 64, "y": 72 }, { "n": 345, "e": 385 }],
    "376": [{ "x": 51, "y": 59 }, { "e": 369 }],
    "377": [{ "x": 57, "y": 50 }, { "n": 300 }],
    "378": [{ "x": 60, "y": 47 }, { "n": 333 }],
    "379": [{ "x": 71, "y": 60 }, { "n": 338, "e": 395 }],
    "380": [{ "x": 65, "y": 70 }, { "n": 424, "w": 206 }],
    "381": [{ "x": 52, "y": 62 }, { "n": 364, "w": 394 }],
    "382": [{ "x": 70, "y": 55 }, { "s": 322, "e": 388 }],
    "383": [{ "x": 51, "y": 58 }, { "e": 330, "w": 495 }],
    "384": [{ "x": 69, "y": 51 }, { "w": 349 }],
    "385": [{ "x": 65, "y": 72 }, { "w": 375 }],
    "386": [{ "x": 70, "y": 59 }, { "e": 414, "w": 240 }],
    "387": [{ "x": 58, "y": 48 }, { "n": 317, "s": 417, "w": 431 }],
    "388": [{ "x": 71, "y": 55 }, { "e": 477, "w": 382 }],
    "389": [{ "x": 56, "y": 51 }, { "e": 300 }],
    "390": [{ "x": 67, "y": 69 }, { "w": 344 }],
    "391": [{ "x": 54, "y": 50 }, { "s": 396, "e": 334, "w": 428 }],
    "392": [{ "x": 66, "y": 70 }, { "s": 344, "e": 462 }],
    "393": [{ "x": 55, "y": 49 }, { "n": 334, "s": 482 }],
    "394": [{ "x": 51, "y": 62 }, { "e": 381 }],
    "395": [{ "x": 72, "y": 60 }, { "s": 403, "e": 421, "w": 379 }],
    "396": [{ "x": 54, "y": 49 }, { "n": 391 }],
    "397": [{ "x": 71, "y": 58 }, { "w": 306 }],
    "398": [{ "x": 70, "y": 56 }, { "e": 438, "w": 360 }],
    "399": [{ "x": 68, "y": 48 }, { "n": 362, "s": 467 }],
    "400": [{ "x": 52, "y": 60 }, { "s": 369 }],
    "401": [{ "x": 67, "y": 50 }, { "w": 358 }],
    "402": [{ "x": 53, "y": 61 }, { "e": 176, "w": 451 }],
    "403": [{ "x": 72, "y": 59 }, { "n": 395 }],
    "404": [{ "x": 58, "y": 72 }, { "n": 481, "w": 350 }],
    "405": [{ "x": 53, "y": 69 }, { "n": 406, "e": 303 }],
    "406": [{ "x": 53, "y": 70 }, { "s": 405, "w": 415 }],
    "407": [{ "x": 66, "y": 49 }, { "s": 496, "w": 370 }],
    "408": [{ "x": 54, "y": 71 }, { "n": 458, "s": 361, "w": 423 }],
    "409": [{ "x": 57, "y": 49 }, { "e": 317 }],
    "410": [{ "x": 61, "y": 74 }, { "s": 291 }],
    "411": [{ "x": 59, "y": 69 }, { "w": 268 }],
    "412": [{ "x": 52, "y": 66 }, { "s": 488, "e": 310 }],
    "413": [{ "x": 62, "y": 48 }, { "n": 321 }],
    "414": [{ "x": 71, "y": 59 }, { "w": 386 }],
    "415": [{ "x": 52, "y": 70 }, { "e": 406, "w": 418 }],
    "416": [{ "x": 70, "y": 62 }, { "s": 270 }],
    "417": [{ "x": 58, "y": 47 }, { "n": 387 }],
    "418": [{ "x": 51, "y": 70 }, { "n": 425, "s": 474, "e": 415 }],
    "419": [{ "x": 51, "y": 56 }, { "e": 276 }],
    "420": [{ "x": 52, "y": 55 }, { "s": 444, "e": 213, "w": 437 }],
    "421": [{ "x": 73, "y": 60 }, { "n": 440, "w": 395 }],
    "422": [{ "x": 55, "y": 71 }, { "n": 426, "s": 302 }],
    "423": [{ "x": 53, "y": 71 }, { "e": 408, "w": 454 }],
    "424": [{ "x": 65, "y": 71 }, { "s": 380, "e": 473 }],
    "425": [{ "x": 51, "y": 71 }, { "s": 418, "w": 469 }],
    "426": [{ "x": 55, "y": 72 }, { "n": 457, "s": 422 }],
    "427": [{ "x": 71, "y": 57 }, { "e": 430, "w": 327 }],
    "428": [{ "x": 53, "y": 50 }, { "e": 391 }],
    "429": [{ "x": 52, "y": 64 }, { "s": 364 }],
    "430": [{ "x": 72, "y": 57 }, { "n": 443, "e": 439, "w": 427 }],
    "431": [{ "x": 57, "y": 48 }, { "e": 387, "w": 492 }],
    "432": [{ "x": 61, "y": 47 }, { "n": 342 }],
    "433": [{ "x": 71, "y": 53 }, { "s": 455, "e": 460, "w": 323 }],
    "434": [{ "x": 65, "y": 48 }, { "n": 370 }],
    "435": [{ "x": 71, "y": 54 }, { "w": 322 }],
    "436": [{ "x": 57, "y": 73 }, { "s": 350 }],
    "437": [{ "x": 51, "y": 55 }, { "e": 420, "w": 497 }],
    "438": [{ "x": 71, "y": 56 }, { "e": 465, "w": 398 }],
    "439": [{ "x": 73, "y": 57 }, { "w": 430 }],
    "440": [{ "x": 73, "y": 61 }, { "s": 421, "w": 476 }],
    "441": [{ "x": 56, "y": 72 }, { "s": 372 }],
    "442": [{ "x": 60, "y": 72 }, { "n": 347 }],
    "443": [{ "x": 72, "y": 58 }, { "s": 430, "e": 471 }],
    "444": [{ "x": 52, "y": 54 }, { "n": 420, "w": 490 }],
    "445": [{ "x": 52, "y": 68 }, { "n": 447, "e": 339, "w": 450 }],
    "446": [{ "x": 68, "y": 68 }, { "e": 466, "w": 331 }],
    "447": [{ "x": 52, "y": 69 }, { "s": 445 }],
    "448": [{ "x": 51, "y": 63 }, { "e": 364 }],
    "449": [{ "x": 56, "y": 49 }, { "n": 341 }],
    "450": [{ "x": 51, "y": 68 }, { "e": 445 }],
    "451": [{ "x": 52, "y": 61 }, { "e": 402, "w": 453 }],
    "452": [{ "x": 60, "y": 74 }, { "s": 347 }],
    "453": [{ "x": 51, "y": 61 }, { "s": 464, "e": 451 }],
    "454": [{ "x": 52, "y": 71 }, { "n": 470, "e": 423 }],
    "455": [{ "x": 71, "y": 52 }, { "n": 433 }],
    "456": [{ "x": 52, "y": 67 }, { "e": 275, "w": 499 }],
    "457": [{ "x": 55, "y": 73 }, { "n": 461, "s": 426 }],
    "458": [{ "x": 54, "y": 72 }, { "s": 408, "w": 459 }],
    "459": [{ "x": 53, "y": 72 }, { "e": 458 }],
    "460": [{ "x": 72, "y": 53 }, { "w": 433 }],
    "461": [{ "x": 55, "y": 74 }, { "s": 457 }],
    "462": [{ "x": 67, "y": 70 }, { "w": 392 }],
    "463": [{ "x": 67, "y": 49 }, { "s": 468, "e": 362 }],
    "464": [{ "x": 51, "y": 60 }, { "n": 453 }],
    "465": [{ "x": 72, "y": 56 }, { "e": 498, "w": 438 }],
    "466": [{ "x": 69, "y": 68 }, { "s": 486, "e": 472, "w": 446 }],
    "467": [{ "x": 68, "y": 47 }, { "n": 399 }],
    "468": [{ "x": 67, "y": 48 }, { "n": 463 }],
    "469": [{ "x": 50, "y": 71 }, { "e": 425 }],
    "470": [{ "x": 52, "y": 72 }, { "s": 454 }],
    "471": [{ "x": 73, "y": 58 }, { "w": 443 }],
    "472": [{ "x": 70, "y": 68 }, { "w": 466 }],
    "473": [{ "x": 66, "y": 71 }, { "e": 494, "w": 424 }],
    "474": [{ "x": 51, "y": 69 }, { "n": 418 }],
    "475": [{ "x": 64, "y": 48 }, { "n": 371, "s": 484 }],
    "476": [{ "x": 72, "y": 61 }, { "e": 440 }],
    "477": [{ "x": 72, "y": 55 }, { "e": 483, "w": 388 }],
    "478": [{ "x": 51, "y": 53 }, { "e": 351 }],
    "479": [{ "x": 68, "y": 63 }, { "w": 205 }],
    "480": [{ "x": 63, "y": 47 }, { "n": 373 }],
    "481": [{ "x": 58, "y": 73 }, { "s": 404 }],
    "482": [{ "x": 55, "y": 48 }, { "n": 393 }],
    "483": [{ "x": 73, "y": 55 }, { "w": 477 }],
    "484": [{ "x": 64, "y": 47 }, { "n": 475 }],
    "485": [{ "x": 69, "y": 50 }, { "w": 352 }],
    "486": [{ "x": 69, "y": 67 }, { "n": 466 }],
    "487": [{ "x": 59, "y": 47 }, { "n": 318, "s": 489 }],
    "488": [{ "x": 52, "y": 65 }, { "n": 412 }],
    "489": [{ "x": 59, "y": 46 }, { "n": 487 }],
    "490": [{ "x": 51, "y": 54 }, { "e": 444, "w": 493 }],
    "491": [{ "x": 52, "y": 52 }, { "n": 351 }],
    "492": [{ "x": 56, "y": 48 }, { "e": 431 }],
    "493": [{ "x": 50, "y": 54 }, { "e": 490 }],
    "494": [{ "x": 67, "y": 71 }, { "w": 473 }],
    "495": [{ "x": 50, "y": 58 }, { "e": 383 }],
    "496": [{ "x": 66, "y": 48 }, { "n": 407 }],
    "497": [{ "x": 50, "y": 55 }, { "e": 437 }],
    "498": [{ "x": 73, "y": 56 }, { "w": 465 }],
    "499": [{ "x": 51, "y": 67 }, { "e": 456 }]
  }
