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
	query = "SELECT email FROM post JOIN user ON post.user=user.email WHERE forum=%s"
	params = (data["forum"],)
	if "since_id" in data and data["since_id"]:
		if type(data["since_id"]) == list:
			query += " AND user.id>=" + data["since_id"][0] + " AND user.id<=" + data["since_id"][1]
		else:
			if type(data["since_id"]) == unicode:
				query += " AND user.id>=" + data["since_id"]
			else:
				raise Exception({"code":"UNCORRECT REQUEST","message":"since_id can't contains more than 2 elements"})
	query += " GROUP BY email"
	if "order" in data and data["order"]:
		query += " ORDER BY user.name " + data["order"]
	else:
		query += " ORDER BY user.name DESC"
	if "limit" in data and data["limit"]:
		query += " LIMIT " + data["limit"]
	userEmails = dbConnection.execQuery(query,params)
	users = []
	if userEmails:
		userEmails = sum(userEmails,())
		dataRequest = {}
		dataRequest["related"] = []
		for userEmail in userEmails:
			dataRequest["user"] = userEmail
			users.append(api.dbOperations.user.details(dataRequest))
	return users