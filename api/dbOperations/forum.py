from api.dbOperations import dbConnection
import api.dbOperations.user
import api.dbOperations.post
import api.dbOperations.thread
from collections import OrderedDict, defaultdict

fields = ("id","name","short_name","user")

class MyException(Exception):
	pass

def create(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	if dbConnection.notExists(entity="forum", identificator="short_name", value=data["short_name"]):
		dbConnection.execQuery("INSERT forum (name,short_name,user) VALUES (%s,%s,%s)",(data["name"],data["short_name"],data["user"], ))
	dataRequest={}
	dataRequest["forum"] = data["short_name"]
	dataRequest["related"] = []
	return details(dataRequest)

def details(data):
	dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
	forum = dbConnection.execQuery("SELECT id,name,short_name,user FROM forum WHERE short_name=%s",(data["forum"], ))
	forum = OrderedDict(zip(fields,forum[0]))
	if "user" in data["related"]:
		dataRequest = {}
		dataRequest["user"] = forum["user"]
		forum["user"] = api.dbOperations.user.details(dataRequest)
	return dbConnection.fieldsToBoolean(forum)

def listPosts(data):
	return api.dbOperations.post.list(data)

def listThreads(data):
	return api.dbOperations.thread.list(data)

def listUsers(data):
	dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
	order = 'DESC'
	if "order" in data and data["order"]:
		order = data["order"]
	if "limit" in data and data["limit"]:
		if "since" in data and data["since"]:
			userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s AND user.id>=%s AND user.id<=%s ORDER BY user.name " + order + " LIMIT " + data["limit"] + ";",(data["forum"], data["since"][0], data["since"][1], ))
		else:
			userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s ORDER BY user.name " + order + " LIMIT " + data["limit"] + ";",(data["forum"], ))
	else:
		if "since" in data and data["since"]:
			userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s AND user.id>=%s AND user.id<=%s ORDER BY user.name " + order + ";",(data["forum"], data["since"][0], data["since"][1], ))
		else:
			userEmails = dbConnection.execQuery("SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s ORDER BY user.name " + order + ";",(data["forum"], ))
	userEmails = sum(userEmails,())
	users = []
	dataRequest = {}
	dataRequest["related"] = []
	for userEmail in userEmails:
		dataRequest["user"] = userEmail
		users.append(api.dbOperations.user.details(dataRequest))
	return users