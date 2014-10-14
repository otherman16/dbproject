import json
from django.http import HttpResponse
import api.dbOperations.forum
from collections import defaultdict

responseTemplate = ("code","response")
codes={"OK":0,"NOT FOUND":1,"INVALID REQUEST":2,"UNCORRECT REQUEST":3,"UNKNOWN ERROR":4,"USER EXISTS":5}

def getResponse(code,response):
	return dict(zip(responseTemplate,(codes[code],response)))

true = True
false = False
null = None

def create(request):
	if request.method == "POST":
		try:
			jsonRequest = json.loads(request.body)
		except:
			dataResponse = getResponse("INVALID REQUEST","Invalid JSON")
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataRequest = {}
		dataRequired = ["name", "short_name", "user"]
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		try:
			forum = api.dbOperations.forum.create(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",forum)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPossible = ["related"]
		dataRequest = {}
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = request.GET.get(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.get(a)
			else:
				dataRequest[a] = []
		try:
			forum = api.dbOperations.forum.details(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",forum)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def listPosts(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPossible = ["since","limit","sort","order","related"]
		dataRequest = defaultdict(list)
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = request.GET.getlist(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.getlist(a)
			else:
				dataRequest[a] = []
		try:
			posts = api.dbOperations.forum.listPosts(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",posts)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def listThreads(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPossible = ["since","limit","order","related"]
		dataRequest = defaultdict(list)
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = request.GET.getlist(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.getlist(a)
			else:
				dataRequest[a] = []
		try:
			threads = api.dbOperations.forum.listThreads(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",threads)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def listUsers(request):
	if request.method == "GET":
		dataRequired = ["forum"]
		dataPossible = ["since","limit","order"]
		dataRequest = defaultdict(list)
		for a in dataRequired:
			if not request.GET.get(a):
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = request.GET.getlist(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.getlist(a)
			else:
				dataRequest[a] = []
		try:
			threads = api.dbOperations.forum.listUsers(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",threads)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')