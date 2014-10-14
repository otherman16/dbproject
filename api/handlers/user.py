import json
from django.http import HttpResponse
import api.dbOperations.user
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
		try:
			jsonRequest = json.loads(request.body)
		except:
			dataResponse = getResponse("INVALID REQUEST","Invalid JSON")
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataRequest = {}
		dataRequired = ["username", "about", "name", "email"]
		dataPosible = ["isAnonymous"]
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			user = api.dbOperations.user.create(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",user)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["user"]
		dataPossible = []
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
			user = api.dbOperations.user.details(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",user)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def follow(request):
	if request.method == "POST":
		try:
			jsonRequest = json.loads(request.body)
		except:
			dataResponse = getResponse("INVALID REQUEST","Invalid JSON")
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataRequest = {}
		dataRequired = ["follower", "followee"]
		dataPosible = []
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			user = api.dbOperations.user.follow(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",user)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def listFollowers(request):
	if request.method == "GET":
		dataRequired = ["user"]
		dataPossible = ["limit","order","since_id"]
		dataRequest = defaultdict(list)
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = request.GET.getlist(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.getlist(a)
			else:
				dataRequest[a] = []
		try:
			followers = api.dbOperations.user.listFollowers(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",followers)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

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
	if request.method == "POST":
		try:
			jsonRequest = json.loads(request.body)
		except:
			dataResponse = getResponse("INVALID REQUEST","Invalid JSON")
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataRequest = {}
		dataRequired = ["follower", "followee"]
		dataPosible = []
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			user = api.dbOperations.user.unfollow(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",user)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def updateProfile(request):
	if request.method == "POST":
		try:
			jsonRequest = json.loads(request.body)
		except:
			dataResponse = getResponse("INVALID REQUEST","Invalid JSON")
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataRequest = {}
		dataRequired = ["about", "user", "name",]
		dataPosible = []
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			user = api.dbOperations.user.update(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",user)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')