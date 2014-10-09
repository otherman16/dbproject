import json
from django.http import HttpResponse
true = True
false = False
null = None

def close(request):
	data = {
				"code": 0,
			    "response": {
			        "thread": 1
			    }
			}
	return HttpResponse(json.dumps(data))

def create(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-01 00:00:01",
			        "forum": "forum1",
			        "id": 1,
			        "isClosed": true,
			        "isDeleted": true,
			        "message": "hey hey hey hey!",
			        "slug": "Threadwithsufficientlylargetitle",
			        "title": "Thread With Sufficiently Large Title",
			        "user": "example3@mail.ru"
			    }
			}
	return HttpResponse(json.dumps(data))

def details(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-01 00:00:01",
			        "dislikes": 0,
			        "forum": "forum1",
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
			}
	return HttpResponse(json.dumps(data))

def list(request):
	data = {
				"code": 0,
			    "response": [
			        {
			            "date": "2014-01-01 00:00:01",
			            "dislikes": 0,
			            "forum": "forum1",
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

def listPosts(request):
	data = {
				"code": 0,
			    "response": [
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
			        },
			        {
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
			    ]
			}
	return HttpResponse(json.dumps(data))

def open(request):
	data = {
				"code": 0,
			    "response": {
			        "thread": 1
			    }
			}
	return HttpResponse(json.dumps(data))

def remove(request):
	data = {
				"code": 0,
			    "response": {
			        "thread": 1
			    }
			}
	return HttpResponse(json.dumps(data))

def restore(request):
	data = {
				"code": 0,
			    "response": {
			        "thread": 1
			    }
			}
	return HttpResponse(json.dumps(data))

def subscribe(request):
	data = {
				"code": 0,
			    "response": {
			        "thread": 4,
			        "user": "richard.nixon@example.com"
			    }
			}
	return HttpResponse(json.dumps(data))

def unsubscribe(request):
	data = {
				"code": 0,
			    "response": {
			        "thread": 1,
			        "user": "example4@mail.ru"
			    }
			}
	return HttpResponse(json.dumps(data))

def update(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-01 00:00:01",
			        "dislikes": 0,
			        "forum": "forum1",
			        "id": 1,
			        "isClosed": false,
			        "isDeleted": false,
			        "likes": 0,
			        "message": "hey hey hey hey!",
			        "points": 0,
			        "posts": 0,
			        "slug": "newslug",
			        "title": "Thread With Sufficiently Large Title",
			        "user": "example3@mail.ru"
			    }
			}
	return HttpResponse(json.dumps(data))

def vote(request):
	data = {
				"code": 0,
			    "response": {
			        "date": "2014-01-01 00:00:01",
			        "dislikes": 0,
			        "forum": "forum1",
			        "id": 1,
			        "isClosed": false,
			        "isDeleted": false,
			        "likes": 1,
			        "message": "hey hey hey hey!",
			        "points": 1,
			        "posts": 0,
			        "slug": "newslug",
			        "title": "Thread With Sufficiently Large Title",
			        "user": "example3@mail.ru"
			    }
			}
	return HttpResponse(json.dumps(data))