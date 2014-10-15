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
	if not (data["forum"] == dbConnection.execQuery("SELECT forum FROM thread WHERE id = %s;", (data["thread"], ))[0][0]):
		raise Exceptions({"code":"INVALID REQUEST","message":"Forum with short_name '" + data["forum"] + "' doesn't contain thread with id '" + str(data["thread"]) + "'"})
	isApproved = False
	isDeleted = False
	isEdited = False
	isHighlighted = False
	isSpam = False
	parent = None
	if "isApproved" in data and data["isApproved"]:
		isApproved = data["isApproved"]
	if "isDeleted" in data and data["isDeleted"]:
		isDeleted = data["isDeleted"]
	if "isEdited" in data and data["isEdited"]:
		isEdited = data["isEdited"]
	if "isHighlighted" in data and data["isHighlighted"]:
		isHighlighted = data["isHighlighted"]
	if "isSpam" in data and data["isSpam"]:
		isSpam = data["isSpam"]
	if "parent" in data and data["parent"]:
		parent = data["parent"]
	path = None
	if parent:
		path = dbConnection.execQuery("SELECT CONCAT((SELECT path FROM post WHERE id = %s),'.',(SELECT COUNT(*)+1 FROM post WHERE parent = %s AND thread = %s));",(parent,parent,data["thread"], ))[0][0]
	else:
		path = dbConnection.execQuery("SELECT COUNT(*)+1 FROM post WHERE ISNULL(parent) AND thread = %s;",(data["thread"], ))[0][0]
	dataRequest={}
	dataRequest["post"] = dbConnection.execQuery("INSERT post (date,forum,isApproved,isDeleted,isEdited,isHighlighted,isSpam,message,parent,thread,user,path) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data["date"],data["forum"],isApproved,isDeleted,isEdited,isHighlighted,isSpam,data["message"],parent,data["thread"],data["user"],path, ))
	dbConnection.execQuery("UPDATE thread SET posts = posts + 1 WHERE id = %s;", (data["thread"], ))
	dataRequest["related"] = []
	return details(dataRequest)

def details(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	post = dbConnection.execQuery("SELECT date,dislikes,forum,id,isApproved,isDeleted,isEdited,isHighlighted,isSpam,likes,message,parent,points,thread,user FROM post WHERE id=%s",(data["post"], ))
	post = OrderedDict(zip(fields,post[0]))
	if "user" in data["related"]:
		dataRequest = {}
		dataRequest["user"] = post["user"]
		dataRequest["related"] = []
		post["user"] = api.dbOperations.user.details(dataRequest)
	if "forum" in data["related"]:
		dataRequest = {}
		dataRequest["forum"] = post["forum"]
		dataRequest["related"] = []
		post["forum"] = api.dbOperations.forum.details(dataRequest)
	if "thread" in data["related"]:
		dataRequest = {}
		dataRequest["thread"] = post["thread"]
		dataRequest["related"] = []
		post["thread"] = api.dbOperations.thread.details(dataRequest)
	post["date"] = post["date"].strftime("%Y-%m-%d %H:%M:%S")
	return dbConnection.fieldsToBoolean(post)

def list(data):
	entity = None
	if "forum" in data:
		dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"])
		entity = "forum"
	if "thread" in data:
		dbConnection.exists(entity="thread", identificator="id", value=data["thread"])
		entity = "thread"
	if "user" in data:
		dbConnection.exists(entity="user", identificator="email", value=data["user"])
		entity = "user"
	entityVal = data[entity]
	since = '2014-01-01 00:00:00'
	order = 'DESC'
	sort = 'flat'
	if "since" in data and data["since"]:
		since = data["since"]
	if "order" in data and data["order"]:
		order = data["order"]
	if "sort" in data and data["sort"]:
		sort = data["sort"]
	if "limit" in data and data["limit"]:
		if sort == 'flat':
			postIds = dbConnection.execQuery("SELECT id FROM post WHERE " + entity + "=%s AND date>%s ORDER BY date " + order + " LIMIT " + data["limit"] + ";",(entityVal, since ))
		else:
			if sort == 'tree':
				postIds = dbConnection.execQuery("SELECT id FROM post WHERE " + entity + "=%s AND date>%s ORDER BY path " + order + " LIMIT " + data["limit"] + ";",(entityVal, since ))
			else:
				if sort == 'parent_tree':
					postIds = dbConnection.execQuery("SELECT id FROM post WHERE " + entity + "=%s AND date>%s AND path LIKE '_' ORDER BY path " + order + " LIMIT " + data["limit"] + ";",(entityVal, since ))
				else:
					raise Exception({"code":"INVALID REQUEST","message":"Invalid method of sorting '" + sort + "'"})
	else:
		if sort == 'flat':
			postIds = dbConnection.execQuery("SELECT id FROM post WHERE " + entity + "=%s AND date>%s ORDER BY date " + order + ";",(entityVal, since, ))
		else:
			if sort == 'tree':
				postIds = dbConnection.execQuery("SELECT id FROM post WHERE " + entity + "=%s AND date>%s ORDER BY path " + order + ";",(entityVal, since, ))
			else:
				if sort == 'parent_tree':
					postIds = dbConnection.execQuery("SELECT id FROM post WHERE " + entity + "=%s AND date>%s AND path LIKE '_' ORDER BY path " + order + ";",(entityVal, since, ))
				else:
					raise Exception({"code":"INVALID REQUEST","message":"Invalid method of sorting '" + sort + "'"})
	postIds = sum(postIds,())
	posts = []
	dataRequest = {}
	dataRequest["related"] = []
	for postId in postIds:
		dataRequest["post"] = postId
		posts.append(api.dbOperations.post.details(dataRequest))
	return posts

def remove(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	if dbConnection.execQuery("SELECT isDeleted FROM post WHERE id = %s;", (data["post"], ))[0][0]:
		raise Exception({"code":"INVALID REQUEST","message":"Post with id '%s' is already deleted" % data["post"]})
	dbConnection.execQuery("UPDATE post SET isDeleted=true WHERE id = %s;", (data["post"], ))
	dbConnection.execQuery("UPDATE thread SET posts = posts - 1 WHERE id = (SELECT thread FROM post WHERE id = %s);", (data["post"], ))
	return OrderedDict(zip(("post",),(data["post"],)))

def restore(data):
	dbConnection.exists(entity="post", identificator="id", value=data["post"])
	if not dbConnection.execQuery("SELECT isDeleted FROM post WHERE id = %s;", (data["post"], ))[0][0]:
		raise Exception({"code":"INVALID REQUEST","message":"Post with id '%s;' doesn't deleted" % data["post"]})
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