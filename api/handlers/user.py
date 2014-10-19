from api import tools
from api.tools import requireGet, requirePost, throwExceptions
from django.http import HttpResponse
import api.dbOperations.user


@requirePost
@throwExceptions
def create(request):
	dataRequired = ["username", "about", "name", "email"]
	dataPosible = ["isAnonymous"]
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	user = api.dbOperations.user.create(dataRequest)
	dataResponse = tools.getResponse("OK",user)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def details(request):
	dataRequired = ["user"]
	dataPosible = []
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	user = api.dbOperations.user.details(dataRequest)
	dataResponse = tools.getResponse("OK",user)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def follow(request):
	dataRequired = ["follower", "followee"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	user = api.dbOperations.user.follow(dataRequest)
	dataResponse = tools.getResponse("OK",user)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listFollowers(request):
	dataRequired = ["user"]
	dataPosible = ["limit","order","since_id"]
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	followers = api.dbOperations.user.listFollowers(dataRequest)
	dataResponse = tools.getResponse("OK",followers)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listFollowing(request):
	dataRequired = ["user"]
	dataPosible = ["limit","order","since_id"]
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	following = api.dbOperations.user.listFollowing(dataRequest)
	dataResponse = tools.getResponse("OK",following)
	return HttpResponse(dataResponse, content_type='application/json')

@requireGet
@throwExceptions
def listPosts(request):
	dataRequired = ["user"]
	dataPosible = ["limit","order","since"]
	dataRelated = []
	dataRequest = {}
	dataRequest = tools.getGetParametersDataRequest(request,dataRequired,dataPosible,dataRelated)
	posts = api.dbOperations.user.listPosts(dataRequest)
	dataResponse = tools.getResponse("OK",posts)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def unfollow(request):
	dataRequired = ["follower", "followee"]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	user = api.dbOperations.user.unfollow(dataRequest)
	dataResponse = tools.getResponse("OK",user)
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def updateProfile(request):
	dataRequired = ["about", "user", "name",]
	dataPosible = []
	dataRequest = {}
	dataRequest = tools.getJsonDataRequest(request,dataRequired,dataPosible)
	user = api.dbOperations.user.update(dataRequest)
	dataResponse = tools.getResponse("OK",user)
	return HttpResponse(dataResponse, content_type='application/json')