# Backend

## Endpoints

Base URL: `https://lambda-mud-18.herokuapp.com`

| Type | Endpoint                | Description                |
| ---- | ----------------------- | -------------------------- |
| POST | `/api-token-auth/`      | Logs in user               |
| POST | `/api/player/`          | Adds user                  |
| GET  | `/api/player/`          | Gets all players info      |
| GET  | `/api/player/:id`       | Gets player info           |
| POST | `/api/playerinventory/` | Adds player inventory      |
| GET  | `/api/playerinventory/` | Gets all players inventory |
| POST | `/api/item/`            | Adds player item           |
| GET  | `/api/item/`            | Gets all players item      |
| POST | `/api/map/`             | Adds a map                 |
| GET  | `/api/map/`             | Gets all maps              |
| GET  | `/api/map/:id`          | Gets map info              |
| POST | `/api/room/`            | Adds room to map           |
| GET  | `/api/room/`            | Gets all rooms             |

#### POST `/api/api-token-auth/`

```json
{ "username": "usernamehere", "password": "passwordhere" }
```

Receive if successful (200 Success) :

```json
{
  "token": "2280db0119231ed5c782e452f6c0dad008f166a5"
}
```

Authorization Header required for any endpoint below:

Key, Value
Authorization, Token 2280db0119231ed5c782e452f6c0dad008f166a5

#### POST `/api/player/`

Example body:

```json
{
  "playername": "testplayer",
  "name": "Test Player",
  "password": "12345",
  "team_id": "1",
  "current_room": "0",
  "cooldown": 20,
  "encumbrance": 10,
  "strength": 2,
  "speed": 3,
  "gold": 3,
  "inventory": 2,
  "status": 2,
  "errors": 1,
  "messages": 9,
  "token": 10
}
```

Receive if successful (201 Created) :

```json
{
  "playername": "testplayer",
  "name": "Test Player",
  "password": "12345",
  "team_id": 1,
  "current_room": 0,
  "cooldown": 20.0,
  "encumbrance": 10,
  "strength": 2,
  "speed": 3,
  "gold": 3,
  "inventory": "2",
  "status": "2",
  "errors": "1",
  "messages": "9",
  "token": "10"
}
```

#### POST `/api/playerinventory/`

Example body:

```json
{
  "player_id": 2,
  "item_id": 1,
  "quantity": 1
}
```

Receive if successful (201 Created) :

```json
{
  "player_id": 2,
  "item_id": 1,
  "quantity": 1
}
```

#### POST `/api/item/`

Example body:

```json
{
  "name": "an item",
  "description": "this is a cool item",
  "weight": 20,
  "itemtype": "hmm",
  "level": 50,
  "exp": 20,
  "attributes": 3
}
```

Receive if successful (201 Created) :

```json
{
  "name": "an item",
  "description": "this is a cool item",
  "weight": 20,
  "itemtype": "hmm",
  "level": 50,
  "exp": 20,
  "attributes": "3"
}
```

#### POST `/api/map/`

Example body:

```json
{ "": "" }
```

Receive if successful (201 Created) :

```json
{ "": "" }
```

#### POST `/api/room/`

Example body:

```json
{
  "map_id": 1,
  "room_id": 2,
  "title": "a room title",
  "description": "this is a description",
  "coordinates": "[0, 1]",
  "elevation": 2,
  "terrain": "mountains",
  "north": 10,
  "south": 9,
  "east": "?",
  "west": 1
}
```

Receive if successful (201 Created) :

```json
{
  "map_id": 1,
  "room_id": 2,
  "title": "a room title",
  "description": "this is a description",
  "coordinates": "[0, 1]",
  "elevation": 2,
  "terrain": "mountains",
  "north": "10",
  "south": "9",
  "east": "?",
  "west": "1"
}
```
