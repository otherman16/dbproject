from django.http import HttpResponse
import json
from api.dbOperations import dbConnection

def index(request):
	return HttpResponse("Hello")

def clear(request):
	if request.method == "POST":
		dataRequest = {"code":0,"response":"OK"}
		dbConnection.clear();
	else:
		dataRequest = {"code":4,"response":"Method = " + request.method}
	return HttpResponse(json.dumps(dataRequest))