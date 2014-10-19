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
	dataRelated = ["user"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	forum = api.dbOperations.forum.details(dataRequest)
	dataResponse = tools.getResponse("OK",forum)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listPosts(request):
	dataRequired = ["forum"]
	dataPosible = ["since","limit","sort","order","related"]
	dataRelated = ["forum","user","thread"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	posts = api.dbOperations.forum.listPosts(dataRequest)
	dataResponse = tools.getResponse("OK",posts)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listThreads(request):
	dataRequired = ["forum"]
	dataPosible = ["since","limit","order","related"]
	dataRelated = ["user","forum"]
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	threads = api.dbOperations.forum.listThreads(dataRequest)
	dataResponse = tools.getResponse("OK",threads)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listUsers(request):
	dataRequired = ["forum"]
	dataPosible = ["since_id","limit","order"]
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	users = api.dbOperations.forum.listUsers(dataRequest)
	dataResponse = tools.getResponse("OK",users)
	return HttpResponse(dataResponse, content_type='application/json')