from api.dbOperations import dbConnection
import api.dbOperations.forum
import api.dbOperations.post
import api.dbOperations.thread
from collections import OrderedDict, defaultdict

fields = ("about","email","followers","following","id","isAnonymous","name","subscriptions","username")

class MyException(Exception):
	pass

def create(data):
	if dbConnection.notExists(entity="user", identificator="email", value=data["email"]):
		isAnonymous = False
		if data["isAnonymous"]:
			isAnonymous = data["isAnonymous"]
		dbConnection.execQuery("INSERT user (username,about,name,email,isAnonymous) VALUES (%s,%s,%s,%s,%s)",(data["username"],data["about"],data["name"],data["email"], isAnonymous, ))
		dataRequest={}
		dataRequest["user"] = data["email"]
		dataRequest["related"] = []
		return details(dataRequest)
	else:
		raise Exception({"code":"USER EXISTS","message":"User with email '" + data["email"] + "' is already exists"})

def details(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	user = dbConnection.execQuery("SELECT about,email,id,isAnonymous,name,username FROM user WHERE email = %s;",(data["user"], ))
	user = user[0]
	userList = list(user)
	userList.insert(2,[])
	userList.insert(3,[])
	userList.insert(7,[])
	user = tuple(userList)
	user = OrderedDict(zip(fields,user))
	followers = dbConnection.execQuery("SELECT email_follower FROM follow where email_following = %s;",(data["user"], ))
	following = dbConnection.execQuery("SELECT email_following FROM follow where email_follower = %s;",(data["user"], ))
	subscriptions = dbConnection.execQuery("SELECT id_subscribing FROM subscribe where email_subscriber = %s;",(data["user"], ))
	if followers:
		user["followers"] = sum(followers,())
	if following:
		user["following"] = sum(following,())
	if subscriptions:
		user["subscriptions"] = sum(subscriptions,())
	return dbConnection.fieldsToBoolean(user)

def follow(data):
	dbConnection.exists(entity="user", identificator="email", value=data["follower"])
	dbConnection.exists(entity="user", identificator="email", value=data["followee"])
	# if not dbConnection.execQuery("SELECT * FROM follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"], )):
	dbConnection.execQuery("INSERT follow (email_follower,email_following) VALUES (%s,%s)",(data["follower"],data["followee"], ))
	# else:
	# 	raise Exception({"code":"INVALID REQUEST","message":"User with email '" + data["follower"] + "' already follows user with email '" + data["followee"] + "'"})
	dataRequest={}
	dataRequest["user"] = data["follower"]
	dataRequest["related"] = []
	return details(dataRequest)

def listFollowers(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	query = "SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s"
	params = (data["user"],)
	if "since_id" in data and data["since_id"]:
		if type(data["since_id"]) == list:
			query += " AND user.id>=" + data["since_id"][0] + " AND user.id<=" + data["since_id"][1]
		else:
			if type(data["since_id"]) == unicode:
				query += " AND user.id>=" + data["since_id"]
			else:
				raise Exception({"code":"UNCORRECT REQUEST","message":"since_id can't contains more than 2 elements"})
	if "order" in data and data["order"]:
		query += " ORDER BY user.name " + data["order"]
	else:
		query += " ORDER BY user.name DESC"
	if "limit" in data and data["limit"]:
		query += " LIMIT " + data["limit"]
	followersEmails = dbConnection.execQuery(query,params)
	followers = []
	if followersEmails:
		followersEmails = sum(followersEmails,())
		dataRequest = {}
		dataRequest["related"] = []
		for followersEmail in followersEmails:
			dataRequest["user"] = followersEmail
			followers.append(api.dbOperations.user.details(dataRequest))
	return followers

def listFollowing(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	query = "SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s"
	params = (data["user"],)
	if "since_id" in data and data["since_id"]:
		if type(data["since_id"]) == list:
			query += " AND user.id>=" + data["since_id"][0] + " AND user.id<=" + data["since_id"][1]
		else:
			if type(data["since_id"]) == unicode:
				query += " AND user.id>=" + data["since_id"]
			else:
				raise Exception({"code":"UNCORRECT REQUEST","message":"since_id can't contains more than 2 elements"})
	if "order" in data and data["order"]:
		query += " ORDER BY user.name " + data["order"]
	else:
		query += " ORDER BY user.name DESC"
	if "limit" in data and data["limit"]:
		query += " LIMIT " + data["limit"]
	followingsEmails = dbConnection.execQuery(query,params)
	followings = []
	if followingsEmails:
		followingsEmails = sum(followingsEmails,())
		dataRequest = {}
		dataRequest["related"] = []
		for followingsEmail in followingsEmails:
			dataRequest["user"] = followingsEmail
			followings.append(api.dbOperations.user.details(dataRequest))
	return followings

def listPosts(data):
	dataRequest = {}
	for a in data:
		dataRequest[a] = data[a]
	dataRequest["related"] = []
	return api.dbOperations.post.list(dataRequest)

def unfollow(data):
	dbConnection.exists(entity="user", identificator="email", value=data["follower"])
	dbConnection.exists(entity="user", identificator="email", value=data["followee"])
	# if dbConnection.execQuery("SELECT * FROM follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"], )):
	dbConnection.execQuery("DELETE FROM follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"], ))
	# else:
	# 	raise Exception({"code":"INVALID REQUEST","message":"User with email '" + data["follower"] + "' doesn't follow user with email '" + data["followee"] + "'"})
	dataRequest={}
	dataRequest["user"] = data["follower"]
	dataRequest["related"] = []
	return details(dataRequest)

def update(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.execQuery("UPDATE user SET about=%s,name=%s WHERE email=%s;", (data["about"],data["name"],data["user"], ))
	dataRequest={}
	dataRequest["user"] = data["user"]
	dataRequest["related"] = []
	return details(dataRequest)