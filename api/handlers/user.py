import json
from django.http import HttpResponse
true = True
false = False
null = None

def create(request):
	data = {
				"code": 0,
			    "response": {
			        "about": "hello im user1",
			        "email": "example@mail.ru",
			        "id": 1,
			        "isAnonymous": false,
			        "name": "John",
			        "username": "user1"
			    }
			}
	return HttpResponse(json.dumps(data))

def details(request):
	data = {
				"code": 0,
			    "response": {
			        "about": "hello im user1",
			        "email": "example@mail.ru",
			        "followers": [
			            "example3@mail.ru"
			        ],
			        "following": [
			            "example3@mail.ru"
			        ],
			        "id": 1,
			        "isAnonymous": false,
			        "name": "John",
			        "subscriptions": [
			            4
			        ],
			        "username": "user1"
			    }
			}
	return HttpResponse(json.dumps(data))

def follow(request):
	data = {
				"code": 0,
			    "response": {
			        "about": "hello im user1",
			        "email": "example@mail.ru",
			        "followers": [
			            "example3@mail.ru"
			        ],
			        "following": [
			            "example3@mail.ru"
			        ],
			        "id": 1,
			        "isAnonymous": false,
			        "name": "John",
			        "subscriptions": [
			            4
			        ],
			        "username": "user1"
			    }
			}
	return HttpResponse(json.dumps(data))

def listFollowers(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "about": "Wowowowow!!!",
			            "email": "example3@mail.ru",
			            "followers": [
			                "example@mail.ru"
			            ],
			            "following": [
			                "example@mail.ru"
			            ],
			            "id": 4,
			            "isAnonymous": false,
			            "name": "NewName2",
			            "subscriptions": [
			                3,
			                1
			            ],
			            "username": "user3"
			        }
			    ]
			}
	return HttpResponse(json.dumps(data))

def listFollowing(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "about": "hello im user1",
			            "email": "example@mail.ru",
			            "followers": [
			                "example3@mail.ru"
			            ],
			            "following": [
			                "example3@mail.ru"
			            ],
			            "id": 1,
			            "isAnonymous": false,
			            "name": "John",
			            "subscriptions": [
			                4
			            ],
			            "username": "user1"
			        }
			    ]
			}
	return HttpResponse(json.dumps(data))

def listPosts(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "date": "2014-01-02 00:02:01",
			            "dislikes": 0,
			            "forum": "forum2",
			            "id": 3,
			            "isApproved": false,
			            "isDeleted": false,
			            "isEdited": true,
			            "isHighlighted": false,
			            "isSpam": true,
			            "likes": 0,
			            "message": "my message 1",
			            "parent": 2,
			            "points": 0,
			            "thread": 4,
			            "user": "example@mail.ru"
			        },
			        {
			            "date": "2014-01-03 00:01:01",
			            "dislikes": 0,
			            "forum": "forum1",
			            "id": 4,
			            "isApproved": true,
			            "isDeleted": false,
			            "isEdited": false,
			            "isHighlighted": false,
			            "isSpam": false,
			            "likes": 0,
			            "message": "my message 1",
			            "parent": null,
			            "points": 0,
			            "thread": 3,
			            "user": "example@mail.ru"
			        }
			    ]
			}
	return HttpResponse(json.dumps(data))

def unfollow(request):
	data = {
				"code": 0,
			    "response": {
			        "about": "hello im user1",
			        "email": "example@mail.ru",
			        "followers": [],
			        "following": [],
			        "id": 1,
			        "isAnonymous": false,
			        "name": "John",
			        "subscriptions": [
			            4
			        ],
			        "username": "user1"
			    }
			}
	return HttpResponse(json.dumps(data))

def updateProfile(request):
	data = {
				"code": 0,
			    "response": {
			        "about": "Wowowowow!!!",
			        "email": "example3@mail.ru",
			        "followers": [],
			        "following": [],
			        "id": 4,
			        "isAnonymous": false,
			        "name": "NewName2",
			        "subscriptions": [
			            3,
			            1
			        ],
			        "username": "user3"
			    }
			}
	return HttpResponse(json.dumps(data))