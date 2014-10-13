from api.dbOperations import dbConnection, user, post, thread
from collections import OrderedDict, defaultdict

fields = ("about","email","followers","following","id","isAnonymous","name","subscriptions","username")

class MyException(Exception):
	pass

def create(data):
	if dbConnection.notExists(entity="user", identificator="email", value=data["email"]):
		isAnonymous = "false"
		if data["isAnonymous"]:
			isAnonymous = data["isAnonymous"]
		dbConnection.execQuery("INSERT user (username,about,name,email,isAnonymous) VALUES (%s,%s,%s,%s)",(data["username"],data["about"],data["name"],data["email"], isAnonymous, ))
		dataRequest={}
		dataRequest["user"] = data["email"]
		return details(dataRequest)

def details(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]):
		user = dbConnection.execQuery("SELECT about,email,id,isAnonymous,name,username FROM user WHERE email = %s;",(data["user"], ))
		userList = list(user[0])
		userList.insert(2,[])
		userList.insert(3,[])
		userList.insert(8,[])
		user = tuple(userList)
		user = OrderedDict(zip(fields,user[0]))
		user["followers"] = list(dbConnection.execQuery("SELECT email_follower FROM follow where email_following = %s;",(data["user"], )))
		user["following"] = list(dbConnection.execQuery("SELECT email_following FROM follow where email_follower = %s;",(data["user"], )))
		user["subscriptions"] = list(dbConnection.execQuery("SELECT id_subscripting FROM follow where email_subscriber = %s;",(data["user"], )))
		return user

def follow(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["follower"]) and dbConnection.exists(entity="user", identificator="email", value=data["followee"]):
		dbConnection.execQuery("INSERT follow (email_follower,email_following) VALUES (%s,%s)",(data["follower"],data["followee"] ))
		dataRequest={}
		dataRequest["user"] = data["follower"]
		return details(dataRequest)

def listFollowers(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]):
		order = 'desc'
		if data["order"]:
			order = data["order"][0]
		if data["limit"]:
			if data["since_id"]:
				followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s AND user.id>%s AND user.id<%s LIMIT %s ORDER BY user.name %s",(data["user"][0], data["since"][0], data["since"][1], data["limit"][0], order, ))
			else:
				followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s LIMIT %s ORDER BY user.name %s",(data["user"][0], data["limit"][0], order, ))
		else:
			if data["since_id"]:
				followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s AND user.id>%s AND user.id<%s ORDER BY user.name %s",(data["user"][0], data["since"][0], data["since"][1], order, ))
			else:
				followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s ORDER BY user.name %s",(data["user"][0], order, ))
		followers = []
		dataRequest = {}
		dataRequest["related"] = []
		for followersEmail in followersEmails:
			dataRequest["user"].append(followersEmail)
			posts.append(api.dbOperations.user.details(dataRequest))
			dataRequest["post"].remove(followersEmail)
		return followers

def listFollowing(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]):
		order = 'desc'
		if data["order"]:
			order = data["order"][0]
		if data["limit"]:
			if data["since_id"]:
				followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s AND user.id>%s AND user.id<%s LIMIT %s ORDER BY user.name %s",(data["user"][0], data["since"][0], data["since"][1], data["limit"][0], order, ))
			else:
				followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s LIMIT %s ORDER BY user.name %s",(data["user"][0], data["limit"][0], order, ))
		else:
			if data["since_id"]:
				followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s AND user.id>%s AND user.id<%s ORDER BY user.name %s",(data["user"][0], data["since"][0], data["since"][1], order, ))
			else:
				followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s ORDER BY user.name %s",(data["user"][0], order, ))
		followings = []
		dataRequest = {}
		dataRequest["related"] = []
		for followingsEmail in followingsEmails:
			dataRequest["user"].append(followingsEmail)
			posts.append(api.dbOperations.user.details(dataRequest))
			dataRequest["post"].remove(followingsEmail)
		return followings

def listPosts(data):
	dataRequest = defaultdict(list)
	for a in data:
		dataRequest[a].append(data[a])
	dataRequest["related"] = []
	return api.dbOperations.post.list(dataRequest)

def unfollow(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["follower"]) and dbConnection.exists(entity="user", identificator="email", value=data["followee"]):
		dbConnection.execQuery("DELETE follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"] ))
		dataRequest={}
		dataRequest["user"] = data["follower"]
		return details(dataRequest)

def update(data):
	if dbConnection.exists(entity="user", identificator="email", value=data["user"]):
		dbConnection.execQuery("UPDATE user SET about=%s,name=%s WHERE email=%s;", (data["about"],data["name"],data["user"] ))
		dataRequest={}
		dataRequest["user"] = data["user"]
		return details(dataRequest)