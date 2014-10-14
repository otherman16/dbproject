from api import tools
from django.http import HttpResponse
import api.dbOperations.thread

def close(request):
	if request.method == "POST":
		dataRequired = ["thread"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.close(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def create(request):
	if request.method == "POST":
		dataRequired = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
		dataPosible = ["isDeleted"]
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.create(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["thread"]
		dataPossible = ["related"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			thread = api.dbOperations.thread.details(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def list(request):
	if request.method == "GET":
		if request.GET.get("forum"):
			dataRequired = ["forum"]
		if request.GET.get("user"):
			if not dataRequired:
				dataResponse = tools.getResponse("INVALID REQUEST","There are two or more entity required")
				return HttpResponse(dataResponse, content_type='application/json')
			dataRequired = ["user"]
		dataPossible = ["since","limit","order"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			threads = api.dbOperations.thread.list(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",threads)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def listPosts(request):
	if request.method == "GET":
		dataRequired = ["thread"]
		dataPossible = ["limit","order","since","order"]
		dataRequest = {}
		try:
			dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		try:
			posts = api.dbOperations.thread.listPosts(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",posts)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def open(request):
	if request.method == "POST":
		dataRequired = ["thread"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.open(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def remove(request):
	if request.method == "POST":
		dataRequired = ["thread"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.remove(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def restore(request):
	if request.method == "POST":
		dataRequired = ["thread"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.restore(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def subscribe(request):
	if request.method == "POST":
		dataRequired = ["thread","user"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			subscribe = api.dbOperations.thread.subscribe(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",subscribe)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def unsubscribe(request):
	if request.method == "POST":
		dataRequired = ["thread","user"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			subscribe = api.dbOperations.thread.unsubscribe(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",subscribe)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def update(request):
	if request.method == "POST":
		dataRequired = ["thread", "slug", "message"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.update(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')

def vote(request):
	if request.method == "POST":
		dataRequired = ["thread", "vote"]
		dataPosible = []
		dataRequest = {}
		try:
			dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		try:
			thread = api.dbOperations.thread.vote(dataRequest)
		except Exception as e:
			e = dict(e.message)
			dataResponse = tools.getResponse(e["code"],e["message"])
			return HttpResponse(dataResponse, content_type='application/json')
		dataResponse = tools.getResponse("OK",thread)
	else:
		dataResponse = tools.getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(dataResponse, content_type='application/json')