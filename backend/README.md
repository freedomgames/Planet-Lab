The Backend
===========
This is the REST service which supports the front-end application.


Quick Start for Development
---------------------------

###Requirements:
* (Optional) homebrew: http://brew.sh - if you are working on a Mac, this will make it easy to install the other requirements.  
  If you're on Linux, you already have a package manager so use that.
* Python 2.7: http://www.python.org 
  (brew install python / sudo apt-get install python)
* pip: https://pypi.python.org/pypi/pip 
  (already included if you do a brew install python / sudo apt-get install python-pip)
* foreman: https://github.com/ddollar/foreman
  (gem install foreman -- if you have Ruby installed)

You'll also need an database.
For light development or front-end work, sqlite is fine (http://www.sqlite.org brew install sqlite / sudo apt-get install sqlite3)
I would recomend using postgresql for real backend development, as that's what we'll be running in production and sqlite doesn't support things like migrations.

###First Run:
* pip install virtualenv
* git clone [git@github.com:freedomgamees/parklab.git](git@github.com:freedomgamees/parklab.git])
* cd parklab
* virtualenv venv
* source venv/bin/activate
* pip install -r backend/requirements.txt
* pip install -r backend/test-requirements.txt
* If you are using sqlite, change the DATABASE\_URL line in the .env file in this directory to read:
```DATABASE_URL=sqlite:///test.db```
* If you are using postgresql, then issue the command: ```createdb parklab```
* foreman start create_db
* foreman start web

The REST service is now available at [http://localhost:5000](http://localhost:5000)

###Subsequent Runs:
* cd parklab
  (if you aren't there already)
* source venv/bin/activate
  (if your shell has not already sourced this file)
* pip install --upgrade -r requirements.txt 
  (if requirements.txt has changed and you need to install new requirements)
* rm -f backend/src/backend/test.db; foreman start create_db
  (if the db schema has changed and you need to flush and recreate your sqlite database)
* foreman start web

###Other Utilities:
* foreman run tests -e .test_env
  runs the unit tests and outputs coverage information (the -e .test_env bit is important!)
* foreman run bash
  gives you a shell session with your environment set up to run the REST service

Resources
=========
The REST service exposes three resources and supports returning JSON or html for GETs.

Units
-----
Units are collections of quests.

###View all units
#### GET /units
Returns the template units\_list.html with the following available parameters:
```
units: a list of units, where each unit in the list has the fields:
  id_: the unit id number
  name: the unit's name
  description: the unit's description
  image_url: the URL for the unit's image
  url: the URL to view the unit
```

If the Accept header is application/json, returns
```json
[
  {
    "url": "/units/1/",
    "description": "unit 1 desc",
    "image_url": "static/unit_1.jpg",
    "id": 1,
    "name": "unit 1"
  },
  {
    "url": "/units/2/",
    "description": "unit 2 desc",
    "image_url": "static/unit_2.jpg",
    "id": 2,
    "name": "unit 2"
  },
]
```

###View a single unit
#### GET /units/\<unit\_id\>/
Returns the template unit.html with the following available parameters:
```
unit: a single unit with the following fields:
  id_: the unit id number
  name: the unit's name
  description: the unit's description
  image_url: the URL for the unit's image
  url: the URL to view the unit
  quests: a list of quests, where each quest has the following fields:
    id_: the quest id number
    name: the quest's name
    description: the quest's description
    image_url: the quest's image url
    video_url: the quest's video url
    url: the URL to view the quest
```
If the Accept header is application/json, returns
```json
{
  "description": "unit 2 desc", 
  "id": 2, 
  "image_url": "/static/unit_2.jpg",
  "name": "unit 2", 
  "quests": [
    {
      "description": "quest 2 desc", 
      "id": 2, 
      "image_url": "/static/quest_2.jpg", 
      "name": "quest snakes", 
      "url": "/units/2/quests/2", 
      "video_url": "video_2"
    }, 
    {
      "description": "quest 3 desc", 
      "id": 3, 
      "image_url": "/static/quest_3.jpg", 
      "name": "quest 3", 
      "url": "/units/2/quests/3", 
      "video_url": "video_3"
    }
  ], 
  "url": "/units/2/"
}
```

###Create a unit
#### POST /units/
Accepts a JSON body of:
```json
{
  "name": "unit 2", 
  "description": "unit 2 desc", 
  "image_name": "unit_2.jpg"
}
```
Returns a JSON response of:
```json
{
  "id": 7, 
  "name": "unit 2", 
  "description": "unit 2 desc", 
  "image_url": "/static/unit_2.jpg",
  "url": "/units/7/"
}
```

###Update a unit
#### PUT /units/\<unit\_id\>/
Accepts a JSON body of:
```json
{
  "name": "unit 2", 
  "description": "unit 2 desc", 
  "image_name": "unit_2.jpg"
}
```
Returns 200 on success.

###Delete a unit
#### DELETE /units/\<unit\_id\>/
Returns 200 on success.

Quests
------
Quests are curricula organized in units with linked refresher questions.

###View all quests in a unit
#### GET /units/\<unit\_id\>/quests/
Returns the template quest\_list.html with the following available parameters:
```
quests: a list of quests, where each quest in the list has the fields:
  id_: the quest id number
  name: the quest's name
  partner_name: the quest's partner name
  scientist_prep: the quest's scientist prep text
  activity_steps: the quest's activity steps text
  field notes: the quest's field notes text
  image_url: the URL for the quest's image
  video_url: the URL for the quest's video
  url: the URL to view the quest
```

If the Accept header is application/json, returns
```json
[
  {
    "scientist_prep": "sp",
    "name": "na",
    "video_url": "vu",
    "partner_name": "pa",
    "activity_steps": "as",
    "image_name": "ia",
    "url": "/units/1/quests/1/",
    "image_url": "/static/ia",
    "field_notes": "fn",
    "id": 1
  },
  {
    "scientist_prep": "sp",
    "name": "na",
    "video_url": "vu",
    "partner_name": "pa",
    "activity_steps": "as",
    "image_name": "ia",
    "url": "/units/1/quests/2/",
    "image_url": "/static/ia",
    "field_notes": "fn",
    "id": 2
  }
]
```

###View a single quest
#### GET /units/\<unit\_id\>/quests/\<quest\_id\>/

Returns the template quest.html with the following available parameters:
```
quests: a single quest with the following fields:
  id_: the quest id number
  name: the quest's name
  partner_name: the quest's partner name
  scientist_prep: the quest's scientist prep text
  activity_steps: the quest's activity steps text
  field notes: the quest's field notes text
  image_url: the URL for the quest's image
  video_url: the URL for the quest's video
  url: the URL to view the quest
  questions: a list of questions, where each questions in the list has the fields:
    question: the text for the question
    answer: the text for the answer
    id: the id number for the question
```

If the Accept header is application/json, returns
```json
{
  "activity_steps": "as", 
  "field_notes": "fn", 
  "id": 1, 
  "image_name": "ia", 
  "image_url": "/static/ia", 
  "name": "na", 
  "partner_name": "pa", 
  "scientist_prep": "sp", 
  "url": "/units/1/quests/1/", 
  "video_url": "vu",
  "questions": [
    {
      "answer": "answer a", 
      "id": 2, 
      "question": "question a"
    }, 
    {
      "answer": "answer b", 
      "id": 3, 
      "question": "question b"
    }
  ], 
}
```

###Create a quest and add it to a unit
#### POST /units/\<unit\_id\>/quests/
Accepts a JSON body of:
```json
{
  "name": "quest 2", 
  "description": "quest 2 desc", 
  "image_name": "quest_2.jpg",
  "video_url": "video_url_2"
}
```
Returns a JSON response of:
```json
{
  "name": "quest 2", 
  "description": "quest 2 desc", 
  "image_url": "/static/quest_2.jpg", 
  "video_url": "video_url_2",
  "id": 4, 
  "url": "/units/1/quests/4/"
}
```

###Update a quest
#### PUT /units/\<unit\_id\>/quests/\<quest\_id\>/
Accepts a JSON body of:
```json
{
  "name": "unit 2", 
  "description": "unit 2 desc", 
  "image_name": "unit_2.jpg",
  "video_url": "vid_url"
}
```
Returns 200 on success.

###Delete a quest
#### DELETE /units/\<unit\_id\>/\<quest\_id\>/
Returns 200 on success.


Quest Questions
---------------
Quest Questions are refresher questions linked to a quest.

###Create a question and add it to a quest
#### POST /units/\<unit\_id\>/quests/\<quest\_id\>/questions/
Accepts a JSON body of:
```json
{
  "question": "some question",
  "answer": "some answer"
}
```
Returns a JSON response of:
```json
{
  "answer": "some answer",
  "question": "some question",
  "id": 4
}
```

###Update a question
#### PUT /units/\<unit\_id\>/quests/\<quest\_id\>/questions/\<question\_id\>/
Accepts a JSON body of:
```json
{
  "question": "some question",
  "answer": "some answer",
  "quest_id": 3
}
```
Returns 200 on success.

###Delete a question
#### DELETE /units/\<unit\_id\>/quests/\<quest\_id\>/questions/\<question\_id\>/
Returns 200 on success.
