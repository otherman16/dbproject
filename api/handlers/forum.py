from api import tools
from api.tools import requireGet, requirePost, throwExceptions
from django.http import HttpResponse
import api.dbOperations.forum

@requirePost
@throwExceptions
def create(request):
	dataRequired = ["name", "short_name", "user"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	forum = api.dbOperations.forum.create(dataRequest)
	dataResponse = tools.getResponse("OK",forum)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def details(request):
	dataRequired = ["forum"]
	dataPosible = ["related"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
	forum = api.dbOperations.forum.details(dataRequest)
	dataResponse = tools.getResponse("OK",forum)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listPosts(request):
	dataRequired = ["forum"]
	dataPosible = ["since","limit","sort","order","related"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
	posts = api.dbOperations.forum.listPosts(dataRequest)
	dataResponse = tools.getResponse("OK",posts)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listThreads(request):
	dataRequired = ["forum"]
	dataPosible = ["since","limit","order","related"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
	threads = api.dbOperations.forum.listThreads(dataRequest)
	dataResponse = tools.getResponse("OK",threads)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listUsers(request):
	dataRequired = ["forum"]
	dataPosible = ["since","limit","order"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible)
	users = api.dbOperations.forum.listUsers(dataRequest)
	dataResponse = tools.getResponse("OK",users)
	return HttpResponse(dataResponse, content_type='application/json')