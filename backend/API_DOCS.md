API Docs
========
Description of the REST service and the API it provides.

Authorization
-------------
Authorization information is stored in cookie-backed sessions.
Redirects to the log-in page will be returned when non-authenticated
sessions attempt to access resources which require authorization.
The log-in flow takes care of creating user resources, obviating
the need for a POST /users end-point.

Static Content
--------------
Static content is stored in Amazon S3 and distributed via Amazon CloudFront.
The front-end is responsible for uploading files to S3, but it must use the
back-end to authorize upload requests.
The front-end must then inform the back-end that the upload is complete and set
the asset url on the affected resource via a PUT or POST.
The following end-points may be used to sign upload requests to S3 for
user-uploaded static assets.

These end-points may be used as follows:
```javascript
var createCORSRequest = function(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);
    return xhr;
  } else if (typeof XDomainRequest != "undefined") {
    // Otherwise, check for XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);
    return xhr;
  } else {
    // Otherwise, CORS is not supported by the browser.
    throw new Error('CORS not supported');
  }
};
var s3_upload = function() {
  var file = document.getElementById('file').files[0];
  $.ajax({
    url: '/v1/s3/sign-avatar-upload',
    data: {file_name: 'avatar', mime_type: file.type},
    success: function(response) {
      var xhr = createCORSRequest('PUT', response.signed_request, true);
      xhr.setRequestHeader('Content-Type', file.type);
      xhr.setRequestHeader('x-amz-acl', 'public-read');
      xhr.send(file);
    }
  });
};
```

####GET /v1/s3/sign-avatar-upload
#####Retrieve a signing key for uploading avatar images
######Required Query String Parameters:
```
file_name: the name the file will be given when uploaded to S3
mime_type: the mime type of the file to be uploaded to S3
```
Returns an object in the form:
```javascript
{
  // the URL to use when uploading the file to S3
  "signed_request": "https://freedomgames.s3.amazonaws.com/avatars/1/avatar?Signature=0nY%2B1WL638WZBwOnxZ3LbKehqQw%3D&Expires=1404321203&AWSAccessKeyId=AKIAJX6VRPXCET57OFSQ&x-amz-acl=public-read", 
  // the URL at which the uploaded file will be available after upload
  "url": "https://freedomgames.s3.amazonaws.com/avatars/3/file_name"
}
```

####GET /v1/s3/sign-quest-upload
#####Retrieve a signing key for uploading avatar images
######Required Query String Parameters:
```
file_name: the name the file will be given when uploaded to S3
mime_type: the mime type of the file to be uploaded to S3
quest_id: id of the quest for which the asset is being uploaded
```
Returns an object in the form:
```javascript
{
  // the URL to use when uploading the file to S3
  "signed_request": "https://freedomgames.s3.amazonaws.com/avatars/1/avatar?Signature=0nY%2B1WL638WZBwOnxZ3LbKehqQw%3D&Expires=1404321203&AWSAccessKeyId=AKIAJX6VRPXCET57OFSQ&x-amz-acl=public-read", 
  // the URL at which the uploaded file will be available after upload
  "url": "https://freedomgames.s3.amazonaws.com/quests/6/file_name"
}
```


Resources
=========
Description of the resources and verbs provided by the REST service.

Users
-----
A user account for either a learner or a mentor.

####GET /v1/users/\<id\>
#####Retrieve the user with the given id
Returns an object in the form:
```javascript
{
  "id": 5,
  "url": "/v1/users/5",
  "name": "Walt",
  "organizations": [
    {
      "id": 3,
      "url": "/v1/organizations/3",
      "name": "Freedom Games",
      "icon_url": "/static/freedom.png"
    }
  ],
  "avatar_url": "/static/happy-cat.png"
}
```

####PUT /v1/users/\<id\>
#####Update the user with the given id
Accepts an object in the form:
```javascript
{
  "name": "Neo Walt",
  "avatar_url": "/static/super-happy-cat.png"
}
```

####DELETE /v1/users/\<id\>
#####Delete the user with the given id


Missions
--------
Missions are groups of quests.
Mentors chose how to group quests into missions and learners complete
missions quest by quest.

####POST /v1/missions/
#####Create a new mission
Accepts an object in the form:
```javascript
{
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5
}
```

Returns an object in the form:
```javascript
{
  "id": 2,
  "url": "/v1/missions/2",
  "creator_id": 5,
  "creator_url": "/v1/users/5",
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5,
  "quests": []
}
```
most notably containing the id for the newly created resource and the url
for manipulating it

####GET /api/users/\<id\>/missions/
#####Return missions created by the user with the given id
Returns an object in the form:
```javascript
{
  "missions": [
    {
      "id": 2,
      "url": "/v1/missions/2",
      "creator_id": 5,
      "creator_url": "/v1/users/5",
      "name": "Garden Expert",
      "description": "Learn how to be a gardener!",
      "points": 5
      "quests": [
        {
          "id": 8,
          "url": "/v1/quests/8",
          "creator_id": 1,
          "creator_url": "/v1/users/1",
          "name": "Tree Science",
          "summary": "Learn all about trees!",
          "icon_url": "/static/tree.png",
        }
      ]
    },
    {
      "id": 4,
      "url": "/v1/missions/4",
      "creator_id": 5,
      "creator_url": "/v1/users/5",
      "name": "Music Man",
      "description": "Learn about sound and music!",
      "points": 2,
      "quests": []
    }
  ]
}
```

####GET /v1/missions/\<id\>
#####Retrieve the mission with the given id
Returns an object in the form:
```javascript
{
  "id": 2,
  "url": "/v1/missions/2",
  "creator_id": 5,
  "creator_url": "/v1/users/5",
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5,
  "quests": [
    {
      "id": 8,
      "url": "/v1/quests/8",
      "creator_id": 1,
      "creator_url": "/v1/users/1",
      "name": "Tree Science",
      "summary": "Learn all about trees!",
      "icon_url": "/static/tree.png",
    }
  ]
}
```

####PUT /v1/missions/\<id\>
#####Update the mission with the given id
Accepts an object in the form:
```javascript
{
  "name": "Garden Expert",
  "description": "Learn how to be a gardener!",
  "points": 5
}
```

####DELETE /v1/missions/\<id\>
#####Delete the mission with the given id


Quests
------
Quests are activities within a mission.
Mentors create quests and link them to missions.
Learners complete quests.

####POST /v1/quests/
#####Create a new quest
Accepts an object in the form:
```javascript
{
  "name": "Flower Planting",
  "summary": "Plant lots of flowers!",
  "inquiry_questions": ["question 1", "question 2"]
  "pbl_description": "learn a lot, please",
  "mentor_guide": "be nice to kids",
  "min_grade_level": 3,
  "max_grade_level": 4,
  "hours_required": 1,
  "minutes_required": 45,
  "icon_url": "/static/flower.png"
  "video_links": ["youtube.com/clouds.mp4", "youtube.com/sun.mp4"]
}
```

Returns an object in the form:
```javascript
{
  "id": 2,
  "url": "/v1/quests/2",
  "creator_id": 5,
  "creator_url": "/v1/users/5",
  "name": "Flower Planting",
  "summary": "Plant lots of flowers!",
  "inquiry_questions": ["question 1", "question 2"]
  "tags": [],
  "pbl_description": "learn a lot, please",
  "mentor_guide": "be nice to kids",
  "min_grade_level": 3,
  "max_grade_level": 4,
  "hours_required": 1,
  "minutes_required": 45,
  "video_links": ["youtube.com/clouds.mp4", "youtube.com/sun.mp4"]
  "icon_url": "/static/flower.png"
}
```
most notably containing the id for the newly created resource and the url
for manipulating it

####GET /api/users/\<id\>/quests/
#####Return quests created by the user with the given id
Returns an object in the form:
```javascript
{
  "quests": [
    {
      "id": 2,
      "url": "/v1/quests/2",
      "creator_id": 5,
      "creator_url": "/v1/users/5",
      "name": "Flower Planting",
      "summary": "Plant lots of flowers!",
      "inquiry_questions": ["question 1", "question 2"]
      "tags": [
        {"name": "a", "id": 1, "url": "/v1/quest-tags/1"},
        {"name": "b", "id": 2, "url": "/v1/quest-tags/2"}
      ],
      "pbl_description": "learn a lot, please",
      "mentor_guide": "be nice to kids",
      "min_grade_level": 3,
      "max_grade_level": 4,
      "hours_required": 1,
      "minutes_required": 45,
      "video_links": ["youtube.com/clouds.mp4", "youtube.com/sun.mp4"],
      "icon_url": "/static/flower.png"
    },
    {
      "id": 4,
      "url": "/v1/quests/4",
      "creator_id": 5,
      "creator_url": "/v1/users/5",
      "name": "Tree Planting",
      "summary": "Plant lots of trees!",
      "inquiry_questions": ["question 1", "question 2"]
      "tags": [],
      "pbl_description": "learn a lot, OR ELSE",
      "mentor_guide": "be TERRIBLE to kids",
      "min_grade_level": 1,
      "max_grade_level": 6,
      "hours_required": 4,
      "minutes_required": 35,
      "video_links": [],
      "icon_url": "/static/tree.png"
    }
  ]
}
```

####GET /v1/quests/\<id\>
#####Retrieve the quest with the given id
Returns an object in the form:
```javascript
{
  "id": 2,
  "url": "/v1/quests/2",
  "creator_id": 5,
  "creator_url": "/v1/users/5",
  "name": "Flower Planting",
  "summary": "Plant lots of flowers!",
  "inquiry_questions": ["question 1", "question 2"]
  "tags": [
    {"name": "a", "id": 1, "url": "/v1/quest-tags/1"},
    {"name": "b", "id": 2, "url": "/v1/quest-tags/2"}
  ],
  "pbl_description": "learn a lot, please",
  "mentor_guide": "be nice to kids",
  "min_grade_level": 3,
  "max_grade_level": 4,
  "hours_required": 1,
  "minutes_required": 45,
  "video_links": ["youtube.com/clouds.mp4", "youtube.com/sun.mp4"]
  "icon_url": "/static/flower.png"
}
```

####PUT /v1/quests/\<id\>
#####Update the quest with the given id
Accepts an object in the form:
```javascript
{
  "name": "Flower Planting",
  "summary": "Plant lots of flowers!",
  "inquiry_questions": ["question 1", "question 2"]
  "pbl_description": "learn a lot, please",
  "mentor_guide": "be nice to kids",
  "min_grade_level": 3,
  "max_grade_level": 4,
  "hours_required": 1,
  "minutes_required": 45,
  "video_links": ["youtube.com/clouds.mp4", "youtube.com/sun.mp4"]
  "icon_url": "/static/flower.png"
}
```

####DELETE /v1/quests/\<id\>
#####Delete the quest with the given id


Quest Tags
----------
Tags linked to quests to make them more searchable.

####POST /v1/quest-tags/
#####Create a new quest tag
Accepts an object in the form:
```javascript
{
  "name": "Physics",
}
```
where "name" must be unique among all tags.

Returns an object in the form:
```javascript
{
  "name": "Physics",
  "id": 1,
  "url": "/v1/quest-tags/1",
  "creator_id": 1,
  "creator_url": "/v1/users/1"
}
```
most notably containing the id for the newly created resource and the url
for manipulating it.

####GET /v1/quest-tags/
#####Retrieve all available tags
Returns an object in the form:
```javascript
{
  "tags": [
    {
      "name": "physics",
      "id": 1,
      "url": "/v1/quest-tags/1",
      "creator_id": 1,
      "creator_url": "/v1/users/1"
    },
    {
      "name": "chemistry",
      "id": 2,
      "url": "/v1/quest-tags/2",
      "creator_id": 1,
      "creator_url": "/v1/users/1"
    }
  ]
}

####GET /v1/quest-tags/\<id\>
#####Retrieve the quest tag with the given id
Returns an object in the form:
```javascript
{
  "name": "Physics",
  "id": 1,
  "url": "/v1/quest-tags/1",
  "creator_id": 1,
  "creator_url": "/v1/users/1"
}
```

####PUT /v1/quest-tags/\<id\>
#####Update the quest tag with the given id
Accepts an object in the form:
```javascript
{
  "name": "Physics",
}
```
where "name" must be unique among all tags.

####DELETE /v1/quest-tags/\<id\>
#####Delete the quest tag with the given id


Quest-Tag Links
---------------
The many-to-many links used to links tags and quests

####PUT /v1/quests/\<id\>/tags/\<id\>
#####Link the quest to the tag with the given ids

####DELETE /v1/quests/\<id\>/tags/\<id\>
#####Un-link the quest from the tag with the given ids


Quest-Mission Links
-------------------
The many-to-many links used to group quests into missions.

####PUT /v1/missions/\<id\>/quests/\<id\>
#####Link the quest to the mission with the given ids

####DELETE /v1/missions/\<id\>/quests/\<id\>
#####Un-link the quest from the mission with the given ids

####GET /v1/missions/\<id\>/quests/
#####List the quests linked to a mission with the given id
Returns an object in the form:
```javascript
{
  "quests": [
    {
      "id": 2,
      "url": "/v1/quests/2",
      "creator_id": 5,
      "creator_url": "/v1/users/5",
      "name": "Flower Planting",
      "summary": "Plant lots of flowers!",
      "inquiry_questions": ["question 1", "question 2"]
      "tags": [
        {"name": "a", "id": 1, "url": "/v1/quest-tags/1"},
        {"name": "b", "id": 2, "url": "/v1/quest-tags/2"}
      ],
      "pbl_description": "learn a lot, please",
      "mentor_guide": "be nice to kids",
      "min_grade_level": 3,
      "max_grade_level": 4,
      "hours_required": 1,
      "minutes_required": 45,
      "icon_url": "/static/flower.png"
    },
    {
      "id": 4,
      "url": "/v1/quests/4",
      "creator_id": 5,
      "creator_url": "/v1/users/5",
      "name": "Tree Planting",
      "summary": "Plant lots of trees!",
      "inquiry_questions": [],
      "tags": [],
      "pbl_description": null,
      "mentor_guide": null,
      "min_grade_level": null,
      "max_grade_level": null,
      "hours_required": null,
      "minutes_required": null,
      "icon_url": "/static/tree.png"
    }
  ]
}
```

Organizations
-------------
An organization is a collection of users.

####POST /v1/organizations/
#####Create a new organization
Accepts an object in the form:
```javascript
{
  "name": "Planeteers",
  "description": "Saving our planet is the thing to do!",
  "icon_url": "/static/happy-earth.png"
}
```

Returns an object in the form:
```javascript
{
  "id": 2,
  "url": "/v1/organizations/2",
  "name": "Planeteers",
  "description": "Saving our planet is the thing to do!",
  "icon_url": "/static/happy-earth.png",
  "members": [],
  "creator_id": 1
  "creator_url": "/v1/users/1",
}
```
most notably containing the id for the newly created resource and the url
for manipulating it

####GET /v1/organizations/\<id\>
#####Retrieve the organization with the given id
Returns an object in the form:
```javascript
{
  "id": 2,
  "url": "/v1/organizations/2",
  "name": "Planeteers",
  "description": "Saving our planet is the thing to do!",
  "icon_url": "/static/happy-earth.png",
  "members": [
    {
      "id": 1,
      "url": "/v1/users/1",
      "name": "Captain Planet",
      "avatar_url": "/static/cpt-planet.png"
    }
  ],
  "creator_id": 1
  "creator_url": "/v1/users/1",
}
```

####PUT /v1/organizations/\<id\>
#####Update the organization with the given id
Accepts an object in the form:
```javascript
{
  "name": "Planeteers",
  "description": "Saving our planet is the thing to do!",
  "icon_url": "/static/happy-earth.png"
}
```

####DELETE /v1/organizations/\<id\>
#####Delete the organization with the given id


User-Organization Links
-----------------------
The many-to-many links used to group users into organizations.

####PUT /v1/organizations/\<id\>/users/\<id\>
#####Link the user to the organization with the given ids

####DELETE /v1/organizations/\<id\>/users/\<id\>
#####Un-link the user from the organization with the given ids


Questions
---------
Evaluations questions linked to quests.

####POST /v1/quests/\<id\>/questions/
#####Create a new question linked to the given quest
Accepts an object in the form:
```javascript
{
  "description": "What is the moon?",
  "question_type": "text" // "upload" | "text"
}
```

Returns an object in the form:
```javascript
{
  "description": "What is the moon?",
  "question_type": "text" // "upload" | "text"
  "id": 2,
  "url": "/v1/quests/1/questions/2",
  "creator_id": 1,
  "creator_url": "/v1/users/1",
  "quest_id": 1,
  "quest_url": "/v1/quests/1"
}
```
most notably containing the id for the newly created resource and the url
for manipulating it

####GET /v1/quests/\<id\>/questions/
#####Return a list of all questions linked to the given quest
Returns an object in the form:
```javascript
{
  "questions": [
    {
      "description": "What is the moon?",
      "question_type": "text" // "upload" | "text"
      "id": 2,
      "url": "/v1/quests/1/questions/2",
      "creator_id": 1,
      "creator_url": "/v1/users/1",
      "quest_id": 1,
      "quest_url": "/v1/quests/1"
    }
  ]
}
```

####GET /v1/quests/\<id\>/questions/\<id\>
#####Retrieve the question with the given id linked to the given quest
Returns an object in the form:
```javascript
{
  "description": "What is the moon?",
  "question_type": "text" // "upload" | "text"
  "id": 1,
  "url": "/v1/quests/1/questions/1",
  "creator_id": 1,
  "creator_url": "/v1/users/1",
  "quest_id": 1,
  "quest_url": "/v1/quests/1"
}
```

####GET /v1/questions/\<id\>
#####Retrieve the question with the given id
Returns an object in the form:
```javascript
{
  "description": "What is the moon?",
  "question_type": "text" // "upload" | "text"
  "id": 1,
  "url": "/v1/quests/1/questions/1",
  "creator_id": 1,
  "creator_url": "/v1/users/1",
  "quest_id": 1,
  "quest_url": "/v1/quests/1"
}
```

####PUT /v1/quests/\<id\>/questions/\<id\>
#####Update the question with the given id
Accepts an object in the form:
```javascript
{
  "description": "What is cheese?",
}
```
Note that the question_type can not be change after resource creation.

####DELETE /v1/quests/\<id\>/questions/\<id\>
#####Delete the question with the given id


Answers
-------
Answers to questions provided by learners.

####POST /v1/questions/\<id\>/answers/
#####Create a new answer linked to the given question
Accepts an object in the form:
```javascript
{
  "answer_text": "The moon is cheese"
}
```
for questions with a question_type of "text" and:
```javascript
{
  "answer_upload_url": "moon.png"
}
```
for questions with a question_type of "upload."

Returns an object in the form:
```javascript
{
  // Only one of these two fields will ever be populated.
  "answer_text": "The moon is cheese",
  "answer_upload_url": None,
  "question_type": "text", // matches the parent's question type
  "id": 1,
  "url": "/v1/questions/1/answers/1",
  "creator_id": 1,
  "creator_url": "/v1/users/1",
  "question_id": 1,
  "question_url": "/v1/questions/1"
}
```
most notably containing the id for the newly created resource and the url
for manipulating it

####GET /v1/questions/\<id\>/answers/
#####Return a list of all answers linked to the given question
Returns an object in the form:
```javascript
{
    "answers": [
        {
            "answer_text": "cats",
            "answer_upload_url": null,
            "question_type": "text",
            "id": 1,
            "url": "/v1/questions/1/answers/1",
            "question_id": 1,
            "question_url": "/v1/questions/1",
            "creator_id": 1,
            "creator_url": "/v1/users/1"
        },
        {
            "answer_text": "more cats",
            "answer_upload_url": null,
            "question_type": "text",
            "id": 2,
            "url": "/v1/questions/1/answers/2",
            "question_id": 1,
            "question_url": "/v1/questions/1",
            "creator_id": 1,
            "creator_url": "/v1/users/1"
        }
    ]
}
```

####GET /v1/questions/\<id\>/answers/\<id\>
#####Retrieve the answer with the given id
Returns an object in the form:
```javascript
{
    "answer_text": "more cats",
    "answer_upload_url": null,
    "question_type": "text",
    "id": 2,
    "url": "/v1/questions/1/answers/2",
    "question_id": 1,
    "question_url": "/v1/questions/1",
    "creator_id": 1,
    "creator_url": "/v1/users/1"
}
```

####PUT /v1/questions/\<id\>/answers/\<id\>
#####Update the answer with the given id
Accepts an object in the form:
```javascript
{
  "answer_text": "The moon is cheese"
}
```
for questions with a question_type of "text" and:
```javascript
{
  "answer_upload_url": "moon.png"
}
```
for questions with a question_type of "upload."

####DELETE /v1/questions/\<id\>/answers/\<id\>
#####Delete the answer with the given id
