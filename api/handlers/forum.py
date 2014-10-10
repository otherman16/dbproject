import json
from django.http import HttpResponse
from api import dbOperations
true = True
false = False
null = None

def create(request):
	if request.method == "POST":
		dataRequest = json.loads(request.body)
		dataRequired = ["name", "short_name", "user"]
		try:
			for a in dataRequired:
				if a not in dataRequest:
					dataResponse = {"code": 4, "response": "There is no element " + a}
			forum = dbOperations.forum.create(name=dataRequest["name"], short_name=dataRequest["short_name"], user=dataRequest["user"])
		except Exception as e:
			dataResponse = {"code": 4, "response": e.message}
		dataResponse = {"code": 0, "response": forum}
	else:
		dataResponse = {"code": 4, "response": "Method = " + request.method}
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')
def details(request):
	data = {
				"code": 0,
			    "response": {
			        "id": 4,
			        "name": "\u0424\u043e\u0440\u0443\u043c \u0422\u0440\u0438",
			        "short_name": "forum3",
			        "user": {
			            "about": "hello im user2",
			            "email": "example2@mail.ru",
			            "followers": [],
			            "following": [],
			            "id": 3,
			            "isAnonymous": false,
			            "name": "Jey",
			            "subscriptions": [],
			            "username": "user2"
			        }
			    }
			}
	return HttpResponse(json.dumps(data))
def listPosts(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "date": "2014-01-03 00:08:01",
			            "dislikes": 0,
			            "forum": {
			                "id": 2,
			                "name": "Forum I",
			                "short_name": "forum1",
			                "user": "example3@mail.ru"
			            },
			            "id": 5,
			            "isApproved": false,
			            "isDeleted": true,
			            "isEdited": false,
			            "isHighlighted": false,
			            "isSpam": false,
			            "likes": 0,
			            "message": "my message 1",
			            "parent": null,
			            "points": 0,
			            "thread": {
			                "date": "2013-12-30 00:01:01",
			                "dislikes": 0,
			                "forum": "forum1",
			                "id": 3,
			                "isClosed": false,
			                "isDeleted": false,
			                "likes": 0,
			                "message": "hey hey!",
			                "points": 0,
			                "posts": 2,
			                "slug": "thread2",
			                "title": "Thread II",
			                "user": "example3@mail.ru"
			            },
			            "user": "richard.nixon@example.com"
			        },
			        {
			            "date": "2014-01-03 00:01:01",
			            "dislikes": 0,
			            "forum": {
			                "id": 2,
			                "name": "Forum I",
			                "short_name": "forum1",
			                "user": "example3@mail.ru"
			            },
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
			            "thread": {
			                "date": "2013-12-30 00:01:01",
			                "dislikes": 0,
			                "forum": "forum1",
			                "id": 3,
			                "isClosed": false,
			                "isDeleted": false,
			                "likes": 0,
			                "message": "hey hey!",
			                "points": 0,
			                "posts": 2,
			                "slug": "thread2",
			                "title": "Thread II",
			                "user": "example3@mail.ru"
			            },
			            "user": "example@mail.ru"
			        }
			    ]
			}
	return HttpResponse(json.dumps(data))
def listThreads(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "date": "2014-01-01 00:00:01",
			            "dislikes": 0,
			            "forum": {
			                "id": 2,
			                "name": "Forum I",
			                "short_name": "forum1",
			                "user": "example3@mail.ru"
			            },
			            "id": 1,
			            "isClosed": true,
			            "isDeleted": true,
			            "likes": 0,
			            "message": "hey hey hey hey!",
			            "points": 0,
			            "posts": 0,
			            "slug": "Threadwithsufficientlylargetitle",
			            "title": "Thread With Sufficiently Large Title",
			            "user": "example3@mail.ru"
			        }
			    ]
			}
	return HttpResponse(json.dumps(data))
def listUsers(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "about": null,
			            "email": "richard.nixon@example.com",
			            "followers": [],
			            "following": [],
			            "id": 2,
			            "isAnonymous": true,
			            "name": null,
			            "subscriptions": [],
			            "username": null
			        },
			        {
			            "about": "hello im user1",
			            "email": "example@mail.ru",
			            "followers": [],
			            "following": [],
			            "id": 1,
			            "isAnonymous": false,
			            "name": "John",
			            "subscriptions": [],
			            "username": "user1"
			        }
			    ]
			}
	return HttpResponse(json.dumps(data))