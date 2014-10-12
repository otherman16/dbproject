import json
from django.http import HttpResponse
import api.dbOperations.forum
from collections import defaultdict

responseTemplate = ("code","response")
codes={"OK":0,"NOT FOUND":1,"INVALID REQUEST":2,"UNCORRECT REQUEST":3,"UNKNOWN ERROR":4,"USER EXISTS":5}

def getResponse(code,response):
	return dict(zip(responseTemplate,(codes[code],response)))

true = True
false = False
null = None

def create(request):
	if request.method == "POST":
		jsonRequest = json.loads(request.body)
		dataRequest = {}
		dataRequired = ["name", "short_name", "user"]
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		try:
			forum = api.dbOperations.forum.create(dataRequest)
		except Exception as e:
			print(e)
			print(e.message)
			print(e.args[1])
			dataResponse = getResponse("UNKNOWN ERROR",e.args[1])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",forum)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPossible = ["related"]
		dataRequest = {}
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = request.GET.get(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.get(a)
			else:
				dataRequest[a] = []
		try:
			forum = api.dbOperations.forum.details(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",forum)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def listPosts(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPossible = ["since","limit","sort","order","related"]
		dataRequest = defaultdict(list)
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a].append(request.GET.get(a))
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a].append(request.GET.get(a))
			else:
				dataRequest[a] = []
		try:
			posts = api.dbOperations.forum.listPosts(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",posts)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')
	
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