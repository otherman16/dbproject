from api import tools
from django.http import HttpResponse
import api.dbOperations.user

def create(request):
	if request.method == "POST":
		dataRequired = ["username", "about", "name", "email"]
		dataPosible = ["isAnonymous"]
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			user = api.dbOperations.user.create(dataRequest)
		except Exception as e:
			print(e)
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",user)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["user"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			user = api.dbOperations.user.details(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",user)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def follow(request):
	if request.method == "POST":
		dataRequired = ["follower", "followee"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			user = api.dbOperations.user.follow(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",user)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listFollowers(request):
	if request.method == "GET":
		dataRequired = ["user"]
		dataPosible = ["limit","order","since_id"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			followers = api.dbOperations.user.listFollowers(dataRequest)
		except Exception as e:
			print(e)
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",followers)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listFollowing(request):
	if request.method == "GET":
		dataRequired = ["user"]
		dataPosible = ["limit","order","since_id"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			following = api.dbOperations.user.listFollowing(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",following)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listPosts(request):
	if request.method == "GET":
		dataRequired = ["user"]
		dataPosible = ["limit","order","since"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			posts = api.dbOperations.user.listPosts(dataRequest)
		except Exception as e:
			print(e)
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",posts)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def unfollow(request):
	if request.method == "POST":
		dataRequired = ["follower", "followee"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			user = api.dbOperations.user.unfollow(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",user)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def updateProfile(request):
	if request.method == "POST":
		dataRequired = ["about", "user", "name",]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			user = api.dbOperations.user.update(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",user)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')