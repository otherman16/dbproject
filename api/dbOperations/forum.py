from api.dbOperations import dbConnection
from collections import OrderedDict, defaultdict

fields = ("id","name","short_name","user")

class MyException(Exception):
	pass

def create(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]):
		dbConnection.execQuery("INSERT forum (name,short_name,user) VALUES (%s,%s,%s)",(data["name"],data["short_name"],data["user"], ))
		forum = dbConnection.execQuery("SELECT id,name,short_name,user FROM forum WHERE short_name=%s",(data["short_name"], ))
		return OrderedDict(zip(fields,forum[0]))

def details(data):
	if dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"]):
		forum = dbConnection.execQuery("SELECT id,name,short_name,user FROM forum WHERE short_name=%s",(data["forum"], ))
		forum = OrderedDict(zip(fields,forum[0]))
		if data["related"]:
			forum[data["related"]] = api.dbOperations.user.details(forum[data["related"]])
		return forum

def listPosts(data):
	if dbConnection.exists(entity="forum", identificator="short_name", value=data["forum"][0]):
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
			postIds = dbConnection.execQuery("SELECT id FROM post WHERE forum=%s AND date>%s LIMIT %s ORDER BY date %s",(data["forum"][0], since, data["limit"][0], order, ))
		else:
			postIds = dbConnection.execQuery("SELECT id FROM post WHERE forum=%s AND date>%s ORDER BY date %s",(data["forum"][0], since, order, ))
		posts = []
		dataRequest = defaultdict(list)
		dataRequest["related"] = data["related"]
		for postId in postIds:
			dataRequest["post"].append(postId)
			posts.append(api.dbOperations.post.details(data))
			dataRequest["post"].remove(postId)
		return posts