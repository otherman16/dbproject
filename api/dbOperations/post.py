from api.dbOperations import dbConnection
import api.dbOperations.user
import api.dbOperations.forum
import api.dbOperations.thread
from collections import OrderedDict, defaultdict

fields = ("date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "parent", "points", "thread", "user")

def create(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
	dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
	if not (data["forum"] == dbConnection.execQuery("SELECT forum FROM thread WHERE id = %s;", (data["thread"], ))[0]):
		raise Exceptions({"code":"INVALID REQUEST","message":"Forum with short_name '%s' doesn't contain thread with id '%s'" % data["forum"], data["thread"]})
	isApproved = "false"
	isDeleted = "false"
	isEdited = "flase"
	isHighlighted = "false"
	isSpam = "false"
	parent = "null"
	if data["isApproved"]:
		isApproved = data["isApproved"]
	if data["isDeleted"]:
		isDeleted = data["isDeleted"]
	if data["isEdited"]:
		isEdited = data["isEdited"]
	if data["isHighlighted"]:
		isHighlighted = data["isHighlighted"]
	if data["isSpam"]:
		isSpam = data["isSpam"]
	if data["parent"]:
		parent = data["parent"]
	dbConnection.execQuery("INSERT post (date,forum,isApproved,isDeleted,isEdited,isHighlighted,isSpam,message,parent,thread,user) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data["date"],data["short_name"],isApproved,isDeleted,isEdited,isHighlighted,isSpam,data["message"],parent,data["thread"],data["user"], ))
	dbConnection.execQuery("UPDATE thread SET posts = posts + 1 WHERE id = %s;", (data["thread"], ))
	dataRequest={}
	dataRequest["post"] = dbConnection.execQuery("SELECT LAST_INSERT_ID();", ())[0]
	dataRequest["related"] = []
	return details(dataRequest)

def details(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	post = dbConnection.execQuery("SELECT date,dislikes,forum,id,isApproved,isDeleted,isEdited,isHighlighted,isSpam,likes,message,parent,points,thread,user FROM post WHERE id=%s",(data["post"], ))
	post = OrderedDict(zip(fields,post[0]))
	if "user" in data["related"]:
		dataRequest = {}
		dataRequest["user"] = post["user"]
		post["user"] = api.dbOperations.user.details(dataRequest)
	if "forum" in data["related"]:
		dataRequest = {}
		dataRequest["forum"] = post["forum"]
		post["forum"] = api.dbOperations.forum.details(dataRequest)
	if "thread" in data["related"]:
		dataRequest = {}
		dataRequest["thread"] = post["thread"]
		post["thread"] = api.dbOperations.thread.details(dataRequest)
	return post

def list(data):
	entity = None
	if data["forum"]:
		dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
		entity = "forum"
	if data["thread"]:
		dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
		entity = "thread"
	if data["user"]:
		dbConnection.exists(entity="user", identificator="email", value=data["user"])
		entity = "user"
	entityVal = data[entity]
	since = '2014-01-01 00:00:00'
	order = 'DESC'
	sort = 'flat'
	if data["since"]:
		since = data["since"]
	if data["order"]:
		order = data["order"]
	if data["sort"]:
		sort = data["sort"]
	if data["limit"]:
		postIds = dbConnection.execQuery("SELECT id FROM post WHERE %s=%s AND date>%s LIMIT %s ORDER BY date %s",(entity, entityVal since, data["limit"], order, ))
	else:
		postIds = dbConnection.execQuery("SELECT id FROM post WHERE %s=%s AND date>%s ORDER BY date %s",(entity, entityVal, since, order, ))
	posts = []
	dataRequest = {}
	dataRequest["related"] = data["related"]
	for postId in postIds:
		dataRequest["post"] = postId
		posts.append(api.dbOperations.post.details(dataRequest))
	return posts

def remove(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	if dbConnection.execQuery("SELECT isDeleted FROM post WHERE id = %s;", (data["post"], )):
		raise Exceptions({"code":"INVALID REQUEST","message":"Post with id '%s' is already deleted" % data["post"]})
	dbConnection.execQuery("UPDATE post SET isDeleted=true WHERE id = %s;", (data["post"], ))
	dbConnection.execQuery("UPDATE thread SET posts = posts - 1 WHERE id = (SELECT thread FROM post WHERE id = %s);", (data["post"], ))
	return OrderedDict(zip(("post",),(data["post"],)))

def restore(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	if not dbConnection.execQuery("SELECT isDeleted FROM post WHERE id = %s;", (data["post"], )):
		raise Exceptions({"code":"INVALID REQUEST","message":"Post with id '%s;' doesn't deleted" % data["post"]})
	dbConnection.execQuery("UPDATE post SET isDeleted=false WHERE id = %s;", (data["post"], ))
	dbConnection.execQuery("UPDATE thread SET posts = posts + 1 WHERE id = (SELECT thread FROM post WHERE id = %s);", (data["post"], ))
	return OrderedDict(zip(("post",),(data["post"],)))

def update(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	dbConnection.execQuery("UPDATE post SET message = %s, isEdited = %s WHERE id = %s;",(data["message"], "true", data["post"], ))
	dataRequest = {}
	dataRequest["post"] = data["post"]
	dataRequest["related"] = []
	return details(dataRequest)

def vote(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	if data["vote"] == 1:
		dbConnection.execQuery("UPDATE post SET likes = likes + 1, points = points + 1 WHERE id=%s;",(data["post"], ))
	else:
		dbConnection.execQuery("UPDATE post SET dislikes = dislikes + 1, points = points - 1 WHERE id=%s;",(data["post"], ))
	dataRequest = {}
	dataRequest["post"] = data["post"]
	dataRequest["related"] = []
	return details(dataRequest)