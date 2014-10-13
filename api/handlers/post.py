import json
from django.http import HttpResponse
import api.dbOperations.post
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
		jsonRequest = json.loads(request.body)
		dataRequired = ["date", "thread", "message", "user", "forum"]
		dataPosible = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
		dataRequest = {}
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			post = api.dbOperations.post.create(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",post)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def details(request):
	if request.method == "GET":
		dataRequired = ["post"]
		dataPossible = ["related"]
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
			post = api.dbOperations.post.details(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",post)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def list(request):
	if request.method == "GET":
		dataRequired1 = ["forum"]
		dataRequired2 = ["thread"]
		dataPossible = ["since","limit","sort","order"]
		dataRequest = defaultdict(list)
		for a in dataRequired1:
			if not request.GET.get(a):
				dataRequest.clear()
				for b in dataRequired2:
					if not request.GET.get(b):
						dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' or '" + b + "' not found in request")
						return HttpResponse(json.dumps(dataResponse), content_type='application/json')
					else:
						dataRequest[b].append(request.GET.get(b)
			else:
				dataRequest[a] = request.GET.getlist(a)
		for a in dataPossible:
			if request.GET.get(a):
				dataRequest[a] = request.GET.getlist(a)
			else:
				dataRequest[a] = []
		try:
			posts = api.dbOperations.post.list(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",posts)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def remove(request):
	if request.method == "POST":
		jsonRequest = json.loads(request.body)
		dataRequired = ["post"]
		dataPosible = []
		dataRequest = {}
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			post = api.dbOperations.post.remove(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",post)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def restore(request):
	if request.method == "POST":
		jsonRequest = json.loads(request.body)
		dataRequired = ["post"]
		dataPosible = []
		dataRequest = {}
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			post = api.dbOperations.post.restore(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",post)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def update(request):
	if request.method == "POST":
		jsonRequest = json.loads(request.body)
		dataRequired = ["post", "message"]
		dataPosible = []
		dataRequest = {}
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			post = api.dbOperations.post.update(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",post)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')

def vote(request):
	if request.method == "POST":
		jsonRequest = json.loads(request.body)
		dataRequired = ["post", "vote"]
		dataPosible = []
		dataRequest = {}
		for a in dataRequired:
			if a not in jsonRequest:
				dataResponse = getResponse("UNCORRECT REQUEST","Element '" + a + "' not found in request")
				return HttpResponse(json.dumps(dataResponse), content_type='application/json')
			else:
				dataRequest[a] = jsonRequest[a]
		for a in dataPosible:
			if a in jsonRequest:
				dataRequest[a] = jsonRequest[a]
			else:
				dataRequest[a] = []
		try:
			post = api.dbOperations.post.vote(dataRequest)
		except Exception as e:
			dataResponse = getResponse("UNKNOWN ERROR",str(e))
			return HttpResponse(json.dumps(dataResponse), content_type='application/json')
		dataResponse = getResponse("OK",post)
	else:
		dataResponse = getResponse("INVALID REQUEST","Request method = '" + request.method + "'")
	return HttpResponse(json.dumps(dataResponse), content_type='application/json')