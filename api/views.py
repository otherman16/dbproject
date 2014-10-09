from django.http import HttpResponse
import json

def index(request):
	return HttpResponse("Hello")

def clear(request):
	data = {'code':0,'response':'OK'}
	return HttpResponse(json.dumps(data))