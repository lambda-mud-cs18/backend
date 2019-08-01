# Backend

## Endpoints

Base URL: `https://lambda-mud-18.herokuapp.com`

| Type | Endpoint                              | Description                                |
| ---- | ------------------------------------- | ------------------------------------------ |
| POST | `/api-token-auth/`                    | Logs in user                               |
| POST | `/api/player/`                        | Creates user                               |
| GET  | `/api/room/`                          | Gets all rooms                             |
| GET  | `/api/room/:id`                       | Gets a room by id                          |
| GET  | `/api/player/`                        | Gets all players info                      |
| GET  | `/player/:playername/go/:room_id`     | Takes player to specified room             |
| GET  | `/player/:playername/unexplored`      | Takes player to unexplored rooms           |
| GET  | `/player/:playername/explore/:length` | Moves player (length) times                |
| GET  | `/player/:playername/mine/`           | Begins mining process for specified player |

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
