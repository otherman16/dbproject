import json
from django.http import HttpResponse

responseTemplate = ("code","response")
codes={"OK":0,"NOT FOUND":1,"INVALID REQUEST":2,"UNCORRECT REQUEST":3,"UNKNOWN ERROR":4,"USER EXISTS":5}

def getResponse(code,response):
	return json.dumps(dict(zip(responseTemplate,(codes[code],response))))

def getJsonDataRequest(request,dataRequired,dataPosible):
	try:
		jsonRequest = json.loads(request.body)
	except:
		raise Exception({"code":"INVALID REQUEST","message":"Invalid JSON"})
	dataRequest = {}
	for a in dataRequired:
		if a not in jsonRequest:
			raise Exception({"code":"INVALID REQUEST","message":"Element '" + a + "' not found in request"})
		else:
			dataRequest[a] = jsonRequest[a]
	for a in dataPosible:
		if a in jsonRequest:
			dataRequest[a] = jsonRequest[a]
		else:
			dataRequest[a] = []
	return dataRequest

def getGetParametersDataRequest(request,dataRequired,dataPossible):
	dataRequest = {}
	for a in dataRequired:
		if not request.GET.get(a):
			raise Exception({"code":"INVALID REQUEST","message":"Element '" + a + "' not found in request"})
		else:
			dataRequest[a] = request.GET.get(a)
	for a in dataPossible:
		if request.GET.getlist(a):
			temp = request.GET.getlist(a)
			if len(temp) > 1:
				dataRequest[a] = []
			else:
				temp = temp[0]
			dataRequest[a] = temp
		else:
			dataRequest[a] = []
	return dataRequest

# Decorator
def requirePost(func):
	def wrapper(request):
		if request.method == "POST":
			return func(request)
		else:
			dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
			return HttpResponse(dataResponse, content_type='application/json')
	return wrapper

# Decorator
def requireGet(func):
	def wrapper(request):
		if request.method == "GET":
			return func(request)
		else:
			dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
			return HttpResponse(dataResponse, content_type='application/json')
	return wrapper

# Decorator
def throwExceptions(func):
	def wrapper(request):
		try:
			return func(request)
		except Exception as e:
			if type(e.message) is dict:
				e = dict(e.message)
				dataResponse = getResponse(e["code"],e["message"])
			else:
				dataResponse = getResponse("UNKNOWN ERROR",e.message)
			return HttpResponse(dataResponse, content_type='application/json')
	return wrapper