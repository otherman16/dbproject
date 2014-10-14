from api import tools
from django.http import HttpResponse
import api.dbOperations.post

def create(request):
	if request.method == "POST":
		dataRequired = ["date", "thread", "message", "user", "forum"]
		dataPosible = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			post = api.dbOperations.post.create(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",post)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["post"]
		dataPossible = ["related"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			post = api.dbOperations.post.details(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",post)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def list(request):
	if request.method == "GET":
		if request.GET.get("forum"):
			dataRequired = ["forum"]
		if request.GET.get("thread"):
			if not dataRequired:
				dataResponse = tools.getResponse("INVALID REQUEST","There are two or more entity required")
				return HttpResponse(dataResponse, content_type='application/json')
			dataRequired = ["thread"]
		if request.GET.get("user"):
			if not dataRequired:
				dataResponse = tools.getResponse("INVALID REQUEST","There are two or more entity required")
				return HttpResponse(dataResponse, content_type='application/json')
			dataRequired = ["user"]
		dataPossible = ["since","limit","sort","order"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			posts = api.dbOperations.post.list(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",posts)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def remove(request):
	if request.method == "POST":
		dataRequired = ["post"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			post = api.dbOperations.post.remove(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",post)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def restore(request):
	if request.method == "POST":
		dataRequired = ["post"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			post = api.dbOperations.post.restore(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",post)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def update(request):
	if request.method == "POST":
		dataRequired = ["post", "message"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			post = api.dbOperations.post.update(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",post)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def vote(request):
	if request.method == "POST":
		dataRequired = ["post", "vote"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			post = api.dbOperations.post.vote(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",post)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')