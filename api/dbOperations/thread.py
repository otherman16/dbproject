from api.dbOperations import dbConnection
import api.dbOperations.user
import api.dbOperations.forum
import api.dbOperations.post
from collections import OrderedDict, defaultdict

fields = ("date", "dislikes", "forum", "id", "isClosed", "isDeleted", "likes", "message", "points", "posts", "slug", "user")

def close(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if dbConnection.execQuery("SELECT isClosed FROM thread WHERE id = %s;", (data["thread"], )):
		raise Exceptions({"code":"INVALID REQUEST","message":"Thread with id '%s' is already closed" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isClosed=true WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def create(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
	isDeleted = "false"
	if data["isDeleted"]:
		isDeleted = data["isDeleted"]
	dbConnection.execQuery("INSERT thread (forum,title,isClosed,user,date,message,slug,isDeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(data["forum"],data["title"],data["isClosed"],data["user"],data["date"],data["message"],data["slug"],isDeleted, ))
	dataRequest={}
	dataRequest["thread"] = dbConnection.execQuery("SELECT LAST_INSERT_ID();", ())[0]
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
	return thread

def list(data):
	entity = None
	if data["forum"]:
		dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
		entity = "forum"
	if data["user"]:
		dbConnection.exists(entity="user", identificator="email", value=data["user"])
		entity = "user"
	entityVal = data[entity]
	since = '2014-01-01 00:00:00'
	order = 'DESC'
	if data["since"]:
		since = data["since"]
	if data["order"]:
		order = data["order"]
	if data["limit"]:
		postIds = dbConnection.execQuery("SELECT id FROM thread WHERE %s=%s AND date>%s LIMIT %s ORDER BY date %s",(entity, entityVal, since, data["limit"], order, ))
	else:
		threadIds = dbConnection.execQuery("SELECT id FROM thread WHERE %s=%s AND date>%s ORDER BY date %s",(entity, entityVal, since, order, ))
	threads = []
	dataRequest = {}
	dataRequest["related"] = []
	for threadId in threadIds:
		dataRequest["thread"] = threadId
		threads.append(api.dbOperations.thread.details(dataRequest))
	return posts

def listPosts(data):
	dataRequest = {}
	for a in data:
		dataRequest[a] = data[a]
	dataRequest["related"] = []
	return api.dbOperations.post.list(dataRequest)

def open(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not dbConnection.execQuery("SELECT isClosed FROM thread WHERE id = %s;", (data["thread"], )):
		raise Exceptions({"code":"INVALID REQUEST","message":"Thread with id '%s' is opened" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isClosed=false WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def remove(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if dbConnection.execQuery("SELECT isDeleted FROM thread WHERE id = %s;", (data["thread"], )):
		raise Exceptions({"code":"INVALID REQUEST","message":"Thread with id '%s' is already deleted" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isDeleted=true WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def restore(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not dbConnection.execQuery("SELECT isDeleted FROM thread WHERE id = %s;", (data["thread"], )):
		raise Exceptions({"code":"INVALID REQUEST","message":"Thread with id '%s' doesn't deleted" % data["thread"]})
	dbConnection.execQuery("UPDATE thread SET isDeleted=false WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def subscribe(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not len(dbConnection.execQuery("SELECT * FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"] )))
		dbConnection.execQuery("INSERT follow (email_subscriber,id_subscribing) VALUES (%s,%s)",(data["user"],data["thread"] ))
		subscribe = dbConnection.execQuery("SELECT id_subscribing,email_subscriber FROM subscribe WHERE id_subscribing = %s AND email_subscriber;",(data["thread"],data["user"] ))
	else:
		raise Exception({"code":"INVALID REQUEST","message":"User with email '%s' already subscribed on thread with id '%s'" % data["follower"], data["followee"]})
	return OrderedDict(zip(("thread","user")),subscribe[0]))

def unsubscribe(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if len(dbConnection.execQuery("SELECT * FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"] )))
		subscribe = dbConnection.execQuery("SELECT id_subscribing,email_subscriber FROM subscribe WHERE id_subscribing = %s AND email_subscriber;",(data["thread"],data["user"] ))
		dbConnection.execQuery("DELETE FROM follow email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"] ))
	else:
		raise Exception({"code":"INVALID REQUEST","message":"User with email '%s' doesn't subscribed on thread with id '%s'" % data["follower"], data["followee"]})
	return OrderedDict(zip(("thread","user")),subscribe[0]))

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
