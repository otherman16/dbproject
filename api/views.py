from django.http import HttpResponse
from api.dbOperations import dbConnection
from api import tools
from tools import requireGet, requirePost, throwExceptions


@requireGet
def index(request):
	return HttpResponse("Hello")

@requirePost
@throwExceptions
def clear(request):
	dbConnection.clear()
	dataResponse = tools.getResponse("OK","OK")
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def createTables(request):
	dbConnection.createTables()
	dataResponse = tools.getResponse("OK","OK")
	return HttpResponse(dataResponse, content_type='application/json')

@requirePost
@throwExceptions
def recreateDatabase(request):
	dbConnection.recreateDatabase()
	dataResponse = tools.getResponse("OK","OK")
	return HttpResponse(dataResponse, content_type='application/json')