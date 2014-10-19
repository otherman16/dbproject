from api import tools
from api.tools import requireGet, requirePost, throwExceptions
from django.http import HttpResponse
import api.dbOperations.thread

@requirePost
@throwExceptions
def close(request):
	dataRequired = ["thread"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.close(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def create(request):
	dataRequired = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
	dataPosible = ["isDeleted"]
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.create(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def details(request):
	dataRequired = ["thread"]
	dataPosible = ["related"]
	dataRelated = ["user","forum"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	thread = api.dbOperations.thread.details(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def list(request):
	dataRequired = []
	if request.GET.get("forum"):
		dataRequired = ["forum"]
	if request.GET.get("user"):
		if dataRequired:
			dataResponse = tools.getResponse("INVALID REQUEST","There are two or more entity required")
			return HttpResponse(dataResponse, content_type='application/json')
		dataRequired = ["user"]
	if not dataRequired:
		dataResponse = tools.getResponse("INVALID REQUEST","There aren't any entity required")
		return HttpResponse(dataResponse, content_type='application/json')
	dataPosible = ["since","limit","order"]
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	threads = api.dbOperations.thread.list(dataRequest)
	dataResponse = tools.getResponse("OK",threads)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listPosts(request):
	dataRequired = ["thread"]
	dataPosible = ["limit","order","since","sort"]
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	posts = api.dbOperations.thread.listPosts(dataRequest)
	dataResponse = tools.getResponse("OK",posts)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def open(request):
	dataRequired = ["thread"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.open(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def remove(request):
	dataRequired = ["thread"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.remove(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def restore(request):
	dataRequired = ["thread"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.restore(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def subscribe(request):
	dataRequired = ["thread","user"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	subscribe = api.dbOperations.thread.subscribe(dataRequest)
	dataResponse = tools.getResponse("OK",subscribe)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def unsubscribe(request):
	dataRequired = ["thread","user"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	subscribe = api.dbOperations.thread.unsubscribe(dataRequest)
	dataResponse = tools.getResponse("OK",subscribe)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def update(request):
	dataRequired = ["thread", "slug", "message"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.update(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def vote(request):
	dataRequired = ["thread", "vote"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	thread = api.dbOperations.thread.vote(dataRequest)
	dataResponse = tools.getResponse("OK",thread)
	return HttpResponse(dataResponse, content_type='application/json')