from api import tools
from api.tools import requireGet, requirePost, throwExceptions
from django.http import HttpResponse
import api.dbOperations.post

@requirePost
@throwExceptions
def create(request):
	dataRequired = ["date", "thread", "message", "user", "forum"]
	dataPosible = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	post = api.dbOperations.post.create(dataRequest)
	dataResponse = tools.getResponse("OK",post)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def details(request):
	dataRequired = ["post"]
	dataPosible = ["related"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
	post = api.dbOperations.post.details(dataRequest)
	dataResponse = tools.getResponse("OK",post)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def list(request):
	dataRequired = []
	if request.GET.get("forum"):
		dataRequired = ["forum"]
	if request.GET.get("thread"):
		if dataRequired:
			dataResponse = tools.getResponse("INVALID REQUEST","There are two or more entity required")
			return HttpResponse(dataResponse, content_type='application/json')
		dataRequired = ["thread"]
	if request.GET.get("user"):
		if dataRequired:
			dataResponse = tools.getResponse("INVALID REQUEST","There are two or more entity required")
			return HttpResponse(dataResponse, content_type='application/json')
		dataRequired = ["user"]
	if not dataRequired:
		dataResponse = tools.getResponse("INVALID REQUEST","There aren't any entity required")
		return HttpResponse(dataResponse, content_type='application/json')
	dataPosible = ["since","limit","sort","order"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
	posts = api.dbOperations.post.list(dataRequest)
	dataResponse = tools.getResponse("OK",posts)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def remove(request):
	dataRequired = ["post"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	post = api.dbOperations.post.remove(dataRequest)
	dataResponse = tools.getResponse("OK",post)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def restore(request):
	dataRequired = ["post"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	post = api.dbOperations.post.restore(dataRequest)
	dataResponse = tools.getResponse("OK",post)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def update(request):
	dataRequired = ["post", "message"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	post = api.dbOperations.post.update(dataRequest)
	dataResponse = tools.getResponse("OK",post)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def vote(request):
	dataRequired = ["post", "vote"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	post = api.dbOperations.post.vote(dataRequest)
	dataResponse = tools.getResponse("OK",post)
	return HttpResponse(dataResponse, content_type='application/json')