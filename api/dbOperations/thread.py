from api.dbOperations import dbConnection
import api.dbOperations.user
import api.dbOperations.forum
import api.dbOperations.post
from collections import OrderedDict, defaultdict

fields = ("date", "dislikes", "forum", "id", "isClosed", "isDeleted", "likes", "message", "points", "posts", "slug", "title", "user")

def close(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
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
	thread = dbConnection.execQuery("SELECT date,dislikes,forum,id,isClosed,isDeleted,likes,message,points,posts,slug,title,user FROM thread WHERE id=%s",(data["thread"], ))
	thread = OrderedDict(zip(fields,thread[0]))
	if "user" in data["related"]:
		dataRequest = {}
		dataRequest["user"] = thread["user"]
		dataRequest["related"] = []
		thread["user"] = api.dbOperations.user.details(dataRequest)
	if "forum" in data["related"]:
		dataRequest = {}
		dataRequest["forum"] = thread["forum"]
		dataRequest["related"] = []
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
	query = "SELECT id FROM thread WHERE " + entity + "=%s"
	params = (data[entity],)
	if "since" in data and data["since"]:
		query += " AND date>=%s"
		params += (data["since"],)
	if "order" in data and data["order"]:
		query += " ORDER BY date " + data["order"]
	else:
		query += " ORDER BY date DESC"
	if "limit" in data and data["limit"]:
		query += " LIMIT " + data["limit"]
	threadIds = dbConnection.execQuery(query,params)
	threads = []
	if threadIds:
		threadIds = sum(threadIds,())
		dataRequest = {}
		if "related" in data:
			dataRequest["related"] = data["related"]
		else:
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
	dbConnection.execQuery("UPDATE thread SET isClosed=False WHERE id = %s;", (data["thread"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def remove(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	dbConnection.execQuery("UPDATE thread SET isDeleted=True WHERE id = %s;", (data["thread"], ))
	postsIds = dbConnection.execQuery("SELECT id FROM post WHERE thread = %s;", (data["thread"], ))
	dataRequest={}
	for postId in postsIds:
		dataRequest["post"] = postId
		dbConnection.execQuery("UPDATE post SET isDeleted = True WHERE id = %s",(dataRequest["post"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def restore(data):
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	dbConnection.execQuery("UPDATE thread SET isDeleted=False WHERE id = %s;", (data["thread"], ))
	postsIds = dbConnection.execQuery("SELECT id FROM post WHERE thread = %s;", (data["thread"], ))
	dataRequest={}
	for postId in postsIds:
		dataRequest["post"] = postId
		dbConnection.execQuery("UPDATE post SET isDeleted = False WHERE id = %s",(dataRequest["post"], ))
	return OrderedDict(zip(("thread",),(data["thread"],)))

def subscribe(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not (dbConnection.execQuery("SELECT COUNT(*) FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"], )))[0][0]:
		dbConnection.execQuery("INSERT subscribe (email_subscriber,id_subscribing) VALUES (%s,%s)",(data["user"],data["thread"], ))
		subscribe = dbConnection.execQuery("SELECT id_subscribing,email_subscriber FROM subscribe WHERE id_subscribing = %s AND email_subscriber = %s;",(data["thread"],data["user"], ))
	return OrderedDict(zip(("thread","user"),subscribe[0]))

def unsubscribe(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if (dbConnection.execQuery("SELECT COUNT(*) FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"], data["thread"], )))[0][0]:
		subscribe = dbConnection.execQuery("SELECT id_subscribing,email_subscriber FROM subscribe WHERE id_subscribing = %s AND email_subscriber = %s;",(data["thread"], data["user"], ))
		dbConnection.execQuery("DELETE FROM subscribe WHERE email_subscriber = %s AND id_subscribing = %s;",(data["user"],data["thread"], ))
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
