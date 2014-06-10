API Docs
========
Description of the resources and verbs provided by the REST service.


Users
-----
A user account for either a learner or a mentor

####POST /api/users/
#####Create a new user
Accepts an object in the form:
```json
{
  "name": "Walt",
  "organization": "Freedom Games",
  "avatar_url": "/static/happy-cat.png"
}
```

Returns an object in the form:
```json
{
  "id": 5,
  "url": "/api/users/5",
  "name": "Walt",
  "organization": "Freedom Games",
  "avatar_url": "/static/happy-cat.png"
}
```
most notably containing the id for the newly created resource and the url
for manipulating it.

####GET /api/users/<id>
#####Retrieve the user with the given id.
Returns an object in the form:
```json
{
  "id": 5,
  "url": "/api/users/5",
  "name": "Walt",
  "organization": "Freedom Games",
  "avatar_url": "/static/happy-cat.png"
}
```

####PUT /api/users/<id>
#####Update the user with the given id.
Accepts an object in the form:
```json
{
  "name": "Neo Walt",
  "organization": "Mecha-Freedom Games",
  "avatar_url": "/static/super-happy-cat.png"
}
```

####DELETE /api/users/<id>
#####Delete the user with the given id.


Missions
--------
Missions are groups of quests.
Mentors chose how to group quests into missions and learners complete
missions quest by quest.

####POST /api/users/<id>/missions/
#####Create a new mission
Accepts an object in the form:
```json
{
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5
}
```

Returns an object in the form:
```json
{
  "id": 2,
  "user_id": 5,
  "url": "/api/users/5/missions/2",
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5
}
```
most notably containing the id for the newly created resource and the url
for manipulating it.

####GET /api/users/<id>/missions/
#####Return missions created by the user with the given id
Returns an object in the form:
```json
{
  "missions": [
    {
      "id": 2,
      "user_id": 5,
      "url": "/api/users/5/missions/2",
      "name": "Garden Expert",
      "description": "Learn how to be a gardener!",
      "points": 5
    },
    {
      "id": 4,
      "user_id": 5,
      "url": "/api/users/5/missions/4",
      "name": "Music Man",
      "description": "Learn about sound and music!",
      "points": 2
    }
  ]
}
```

####GET /api/users/<id>/missions/<id>
#####Retrieve the mission with the given id.
Returns an object in the form:
```json
{
  "id": 2,
  "user_id": 5,
  "url": "/api/users/5/missions/2",
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5
}
```

####PUT /api/users/<id>/missions/<id>
#####Update the mission with the given id.
Accepts an object in the form:
```json
{
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5
}
```

####DELETE /api/users/<id>/missions/<id>
#####Delete the mission with the given id.


Quests
------
Quests are activities within a mission.
Mentors create quests and link them to missions.
Learners complete quests.

####POST /api/users/<id>/quests/
#####Create a new quest
Accepts an object in the form:
```json
{
  "name": "Flower Planting",
  "description": "Plant lots of flowers!",
  "icon_url": "/static/flower.png"
}
```

Returns an object in the form:
```json
{
  "id": 2,
  "user_id": 5,
  "url": "/api/users/5/quests/2",
  "name": "Flower Planting",
  "description": "Plant lots of flowers!",
  "icon_url": "/static/flower.png"
}
```
most notably containing the id for the newly created resource and the url
for manipulating it.

####GET /api/users/<id>/quests/
#####Return quests created by the user with the given id
Returns an object in the form:
```json
{
  "quests": [
    {
      "id": 2,
      "user_id": 5,
      "url": "/api/users/5/quests/2",
      "name": "Flower Planting",
      "description": "Plant lots of flowers!",
      "icon_url": "/static/flower.png"
    },
    {
      "id": 4,
      "user_id": 5,
      "url": "/api/users/5/quests/4",
      "name": "Tree Planting",
      "description": "Plant lots of trees!",
      "icon_url": "/static/tree.png"
    }
  ]
}
```

####GET /api/users/<id>/quests/<id>
#####Retrieve the quest with the given id.
Returns an object in the form:
```json
{
  "id": 2,
  "user_id": 5,
  "url": "/api/users/5/quests/2",
  "name": "Flower Planting",
  "description": "Plant lots of flowers!",
  "icon_url": "/static/flower.png"
}
```

####PUT /api/users/<id>/quests/<id>
#####Update the quest with the given id.
Accepts an object in the form:
```json
{
  "name": "Flower Planting",
  "description": "Plant lots of flowers!",
  "icon_url": "/static/flower.png"
}
```

####DELETE /api/users/<id>/quests/<id>
#####Delete the quest with the given id.


Quest-Mission Links
-------------------
The many-to-many links used to group quests into missions.

####PUT /api/users/<id>/missions/<id>/quests/<id>
#####Link the quest to the mission with the given ids

####DELETE /api/users/<id>/missions/<id>/quests/<id>
#####Un-link the quest from the mission with the given ids

####GET /api/users/<id>/missions/<id>/quests/
#####List the quests linked to a mission with the given id
Returns an object in the form:
```json
{
  "quests": [
    {
      "id": 2,
      "user_id": 5,
      "url": "/api/users/5/quests/2",
      "name": "Flower Planting",
      "description": "Plant lots of flowers!",
      "icon_url": "/static/flower.png"
    },
    {
      "id": 4,
      "user_id": 5,
      "url": "/api/users/5/quests/4",
      "name": "Tree Planting",
      "description": "Plant lots of trees!",
      "icon_url": "/static/tree.png"
    }
  ]
}
```
