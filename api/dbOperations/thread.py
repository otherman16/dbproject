from api.dbOperations import dbConnection
import api.dbOperations.user
import api.dbOperations.forum
import api.dbOperations.post
from collections import OrderedDict, defaultdict

fields = ("date", "dislikes", "forum", "id", "isClosed", "isDeleted", "likes", "message", "points", "posts", "slug", "user")

def close(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if dbConnection.execQuery("SELECT isClosed FROM thread WHERE id = %s;", (data["thread"], ))[0][0]:
		raise Exception({"code":"INVALID REQUEST","message":"Thread with id '%s' is already closed" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isClosed=true WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def create(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
	isDeleted = "false"
	if data["isDeleted"]:
		isDeleted = data["isDeleted"]
	dataRequest={}
	dataRequest["thread"] = dbConnection.execQuery("INSERT thread (forum,title,isClosed,user,date,message,slug,isDeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(data["forum"],data["title"],data["isClosed"],data["user"],data["date"],data["message"],data["slug"],isDeleted, ))
	dataRequest["related"] = []
	return details(dataRequest)

def details(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	thread = dbConnection.execQuery("SELECT date,dislikes,forum,id,isClosed,isDeleted,likes,message,points,posts,slug,user FROM thread WHERE id=%s",(data["thread"], ))
	thread = OrderedDict(zip(fields,thread[0]))
	if "user" in data["related"]:
		dataRequest = {}
		dataRequest["user"] = thread["user"]
		thread["user"] = api.dbOperations.user.details(dataRequest)
	if "forum" in data["related"]:
		dataRequest = {}
		dataRequest["forum"] = thread["forum"]
		thread["forum"] = api.dbOperations.forum.details(dataRequest)
	thread["date"] = thread["date"].strftime("%Y-%m-%d %H:%M:%S")
	return dbConnection.fieldsToBoolean(thread)

def list(data):
	entity = None
	if "forum" in data and data["forum"]:
		dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
		entity = "forum"
	if "user" in data and data["user"]:
		dbConnection.exists(entity="user", identificator="email", value=data["user"])
		entity = "user"
	entityVal = data[entity]
	since = '2014-01-01 00:00:00'
	order = 'DESC'
	if "since" in data and data["since"]:
		since = data["since"]
	if "order" in data and data["order"]:
		order = data["order"]
	if "limit" in data and data["limit"]:
		threadIds = dbConnection.execQuery("SELECT id FROM thread WHERE " + entity + "=%s AND date>%s " + " ORDER BY date " + order + " LIMIT " + data["limit"] + ";",(entityVal, since, ))
	else:
		threadIds = dbConnection.execQuery("SELECT id FROM thread WHERE " + entity + "=%s AND date>%s ORDER BY date " + order + ";",(entityVal, since, ))
	threadIds = sum(threadIds,())
	threads = []
	dataRequest = {}
	dataRequest["related"] = []
	for threadId in threadIds:
		dataRequest["thread"] = threadId
		threads.append(api.dbOperations.thread.details(dataRequest))
	return threads

def listPosts(data):
	dataRequest = {}
	for a in data:
		dataRequest[a] = data[a]
	dataRequest["related"] = []
	return api.dbOperations.post.list(dataRequest)

def open(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not dbConnection.execQuery("SELECT isClosed FROM thread WHERE id = %s;", (data["thread"], ))[0][0]:
		raise Exception({"code":"INVALID REQUEST","message":"Thread with id '%s' is opened" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isClosed=false WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def remove(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if dbConnection.execQuery("SELECT isDeleted FROM thread WHERE id = %s;", (data["thread"], ))[0][0]:
		raise Exception({"code":"INVALID REQUEST","message":"Thread with id '%s' is already deleted" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isDeleted=true WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def restore(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not dbConnection.execQuery("SELECT isDeleted FROM thread WHERE id = %s;", (data["thread"], ))[0][0]:
		raise Exception({"code":"INVALID REQUEST","message":"Thread with id '%s' doesn't deleted" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isDeleted=false WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def subscribe(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not (dbConnection.execQuery("SELECT COUNT(*) FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"] )))[0][0]:
		dbConnection.execQuery("INSERT subscribe (email_subscriber,id_subscribing) VALUES (%s,%s)",(data["user"],data["thread"] ))
		subscribe = dbConnection.execQuery("SELECT id_subscribing,email_subscriber FROM subscribe WHERE id_subscribing = %s AND email_subscriber = %s;",(data["thread"],data["user"] ))
	else:
		raise Exception({"code":"INVALID REQUEST","message":"User with email '" + data["user"] + "' already subscribed on thread with id '" + str(data["thread"]) + "'"})
	return OrderedDict(zip(("thread","user"),subscribe[0]))

def unsubscribe(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if (dbConnection.execQuery("SELECT COUNT(*) FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"], data["thread"], )))[0][0]:
		subscribe = dbConnection.execQuery("SELECT id_subscribing,email_subscriber FROM subscribe WHERE id_subscribing = %s AND email_subscriber = %s;",(data["thread"], data["user"], ))
		dbConnection.execQuery("DELETE FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"] ))
	else:
		raise Exception({"code":"INVALID REQUEST","message":"User with email '" + data["user"] + "' doesn't subscribed on thread with id '" + str(data["thread"]) + "'"})
	return OrderedDict(zip(("thread","user"),subscribe[0]))

def update(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	dbConnection.execQuery("UPDATE thread SET message = %s, slug = %s WHERE id = %s;",(data["message"], data["slug"], data["thread"], ))
	dataRequest = {}
	dataRequest["thread"] = data["thread"]
	dataRequest["related"] = []
	return details(dataRequest)

def vote(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if data["vote"] == 1:
		dbConnection.execQuery("UPDATE thread SET likes = likes + 1, points = points + 1 WHERE id=%s;",(data["thread"], ))
	else:
		dbConnection.execQuery("UPDATE thread SET dislikes = dislikes + 1, points = points - 1 WHERE id=%s;",(data["thread"], ))
	dataRequest = {}
	dataRequest["thread"] = data["thread"]
	dataRequest["related"] = []
	return details(dataRequest)
