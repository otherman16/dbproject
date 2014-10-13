from django.http import HttpResponse
import json
from api.dbOperations import dbConnection

responseTemplate = ("code","response")
codes={"OK":0,"NOT FOUND":1,"INVALID REQUEST":2,"UNCORRECT REQUEST":3,"UNKNOWN ERROR":4,"USER EXISTS":5}

def getResponse(code,response):
	return dict(zip(responseTemplate,(codes[code],response)))

def index(request):
	return HttpResponse("Hello")

def clear(request):
	if request.method == "POST":
		try:
			dbConnection.clear()
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK","OK")
		return HttpResponse(json.dumps(dataResponse), content_type='application/json')
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def createTables(request):
	if request.method == "POST":
		try:
			dbConnection.createTables()
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK","OK")
		return HttpResponse(json.dumps(dataResponse), content_type='application/json')
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def recreateDatabase(request):
	if request.method == "POST":
		try:
			dbConnection.recreateDatabase()
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK","OK")
		return HttpResponse(json.dumps(dataResponse), content_type='application/json')
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')