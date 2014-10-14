from api.dbOperations import dbConnection
import api.dbOperations.user
import api.dbOperations.forum
import api.dbOperations.thread
from collections import OrderedDict, defaultdict

fields = ("date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "parent", "points", "thread", "user")

def create(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]) and dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"]) and dbConnection.exists(entity="thread", identificator="id", value=data["thread"]):
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
		dataRequest={}
		dataRequest["post"] = dbConnection.execQuery("SELECT LAST_INSERT_ID();", ())[0]
		dataRequest["related"] = []
		return details(dataRequest)

def details(data):
	if dbConnection.exists(entity="post", identificator="id", value=data["post"]):
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
		if dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"][0]):
			entity = "forum"
	else:
		if data["thread"]:
			if dbConnection.exists(entity="thread", identificator="id", value=data["thread"][0]):
				entity = "thread"
		else:
			if data["user"]:
				if dbConnection.exists(entity="user", identificator="email", value=data["user"][0]):
					entity = "user"
	since = '2014-01-01 00:00:00'
	order = 'desc'
	sort = 'flat'
	if data["since"]:
		since = data["since"][0]
	if data["order"]:
		order = data["order"][0]
	if data["sort"]:
		sort = data["sort"][0]
	if data["limit"]:
		postIds = dbConnection.execQuery("SELECT id FROM post WHERE %s=%s AND date>%s LIMIT %s ORDER BY date %s",(entity, data["forum"][0], since, data["limit"][0], order, ))
	else:
		postIds = dbConnection.execQuery("SELECT id FROM post WHERE %s=%s AND date>%s ORDER BY date %s",(entity, data["forum"][0], since, order, ))
	posts = []
	dataRequest = defaultdict(list)
	dataRequest["related"] = data["related"]
	for postId in postIds:
		dataRequest["post"].append(postId)
		posts.append(api.dbOperations.post.details(dataRequest))
		dataRequest["post"].remove(postId)
	return posts

def remove(data):
	if dbConnection.exists(entity="post", identificator="id", value=data["post"]):
		dbConnection.execQuery("UPDATE post SET isDeleted=true WHERE id=%s;",(data["post"], ))
		return OrderedDict(zip(("post",),(data["post"],)))

def restore(data):
	if dbConnection.exists(entity="post", identificator="id", value=data["post"]):
		dbConnection.execQuery("UPDATE post SET isDeleted=false WHERE id=%s;",(data["post"], ))
		return OrderedDict(zip(("post",),(data["post"],)))

def update(data):
	if dbConnection.exists(entity="post", identificator="id", value=data["post"]):
		dbConnection.execQuery("UPDATE post SET message=%s WHERE id=%s;",(data["message"], data["post"], ))
		dataRequest = defaultdict(list)
		dataRequest["post"].append(data["post"])
		dataRequest["related"] = []
		return details(dataRequest)

def vote(data):
	if dbConnection.exists(entity="post", identificator="id", value=data["post"]):
		if data["vote"] == 1:
			dbConnection.execQuery("UPDATE post SET likes = likes + 1, points = points + 1 WHERE id=%s;",(data["post"], ))
		else:
			dbConnection.execQuery("UPDATE post SET dislikes = dislikes + 1, points = points - 1 WHERE id=%s;",(data["post"], ))
		dataRequest = defaultdict(list)
		dataRequest["post"].append(data["post"])
		dataRequest["related"] = []
		return details(dataRequest)