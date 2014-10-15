import json

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