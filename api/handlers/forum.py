from api import tools
from django.http import HttpResponse
import api.dbOperations.forum

def create(request):
	if request.method == "POST":
		dataRequired = ["name", "short_name", "user"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			forum = api.dbOperations.forum.create(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",forum)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPosible = ["related"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			forum = api.dbOperations.forum.details(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",forum)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listPosts(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPosible = ["since","limit","sort","order","related"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			posts = api.dbOperations.forum.listPosts(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",posts)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listThreads(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPosible = ["since","limit","order","related"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			threads = api.dbOperations.forum.listThreads(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",threads)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listUsers(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPosible = ["since","limit","order"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			users = api.dbOperations.forum.listUsers(dataRequest)
		except Exception as e:
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",users)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')