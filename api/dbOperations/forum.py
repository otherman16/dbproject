from api.dbOperations import dbConnection, user, post, thread
from collections import OrderedDict, defaultdict

fields = ("id","name","short_name","user")

class MyException(Exception):
	pass

def create(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]):
		if dbConnection.notExists(entity="forum", identificator="short_name", value=data["short_name"]):
			dbConnection.execQuery("INSERT forum (name,short_name,user) VALUES (%s,%s,%s)",(data["name"],data["short_name"],data["user"], ))
		dataRequest={}
		dataRequest["forum"] = data["short_name"]
		dataRequest["related"] = []
		return details(dataRequest)

def details(data):
	if dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"]):
		forum = dbConnection.execQuery("SELECT id,name,short_name,user FROM forum WHERE short_name=%s",(data["forum"], ))
		forum = OrderedDict(zip(fields,forum[0]))
		if data["related"]:
			dataRequest = {}
			dataRequest["user"] = forum["user"]
			forum["user"] = api.dbOperations.user.details(dataRequest)
		return forum

def listPosts(data):
	return api.dbOperations.post.list(data)

def listThreads(data):
	if dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"][0]):
		since = '2014-01-01 00:00:00'
		order = 'desc'
		if data["since"]:
			since = data["since"][0]
		if data["order"]:
			order = data["order"][0]
		if data["limit"]:
			threadIds = dbConnection.execQuery("SELECT id FROM thread WHERE forum=%s AND date>%s LIMIT %s ORDER BY date %s",(data["forum"][0], since, data["limit"][0], order, ))
		else:
			threadIds = dbConnection.execQuery("SELECT id FROM thread WHERE forum=%s AND date>%s ORDER BY date %s",(data["forum"][0], since, order, ))
		threads = []
		dataRequest = defaultdict(list)
		dataRequest["related"] = data["related"]
		for threadId in threadIds:
			dataRequest["thread"].append(threadId)
			threads.append(api.dbOperations.thread.details(dataRequest))
			dataRequest["thread"].remove(threadId)
		return threads

def listUsers(data):
	if dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"][0]):
		order = 'desc'
		if data["order"]:
			order = data["order"][0]
		if data["limit"]:
			if data["since"]:
				userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s AND user.id>=%s AND user.id<=%s LIMIT %s ORDER BY user.name %s",(data["forum"][0], data["since"][0], data["since"][1], data["limit"][0], order, ))
			else:
				userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s LIMIT %s ORDER BY user.name %s",(data["forum"][0], data["limit"][0], order, ))
		else:
			if data["since"]:
				userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s AND user.id>=%s AND user.id<=%s ORDER BY user.name %s",(data["forum"][0], data["since"][0], data["since"][1], order, ))
			else:
				userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s ORDER BY user.name %s",(data["forum"][0], order, ))
		users = []
		dataRequest = {}
		for userEmail in userEmails:
			dataRequest["user"] = userEmail
			users.append(api.dbOperations.user.details(dataRequest))
		return users