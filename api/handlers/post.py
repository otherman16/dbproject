import json
from django.http import HttpResponse
true = True
false = False
null = None

def create(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-01 00:00:01",
			        "forum": "forum2",
			        "id": 1,
			        "isApproved": true,
			        "isDeleted": false,
			        "isEdited": true,
			        "isHighlighted": true,
			        "isSpam": false,
			        "message": "my message 1",
			        "parent": null,
			        "thread": 4,
			        "user": "example@mail.ru"
			    }
			}
	return HttpResponse(json.dumps(data))

def details(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-02 00:02:01",
			        "dislikes": 0,
			        "forum": "forum2",
			        "id": 3,
			        "isApproved": false,
			        "isDeleted": true,
			        "isEdited": true,
			        "isHighlighted": false,
			        "isSpam": true,
			        "likes": 0,
			        "message": "my message 1",
			        "parent": 2,
			        "points": 0,
			        "thread": 4,
			        "user": "example@mail.ru"
			    }
			}
	return HttpResponse(json.dumps(data))

def list(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "date": "2014-01-03 00:08:01",
			            "dislikes": 0,
			            "forum": "forum1",
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
			            "thread": 3,
			            "user": "richard.nixon@example.com"
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

def remove(request):
	data = {
				"code": 0,
			    "response": {
			        "post": 3
			    }
			}
	return HttpResponse(json.dumps(data))

def restore(request):
	data = {
				"code": 0,
			    "response": {
			        "post": 3
			    }
			}
	return HttpResponse(json.dumps(data))

def update(request):
	data = {
				"code": 0,
			    "response": {
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
			    }
			}
	return HttpResponse(json.dumps(data))

def vote(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-03 00:08:01",
			        "dislikes": 1,
			        "forum": "forum1",
			        "id": 5,
			        "isApproved": false,
			        "isDeleted": true,
			        "isEdited": false,
			        "isHighlighted": false,
			        "isSpam": false,
			        "likes": 0,
			        "message": "my message 1",
			        "parent": null,
			        "points": -1,
			        "thread": 3,
			        "user": "richard.nixon@example.com"
			    }
			}
	return HttpResponse(json.dumps(data))