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
	if not dbConnection.execQuery("SELECT * FROM follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"] )):
		dbConnection.execQuery("INSERT follow (email_follower,email_following) VALUES (%s,%s)",(data["follower"],data["followee"] ))
	else:
		raise Exception({"code":"INVALID REQUEST","message":"User with email '" + data["follower"] + "' already follows user with email '" + data["followee"] + "'"})
	dataRequest={}
	dataRequest["user"] = data["follower"]
	return details(dataRequest)

def listFollowers(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	order = "DESC"
	if "order" in data and data["order"]:
		order = data["order"]
	if "limit" in data and data["limit"]:
		if "since_id" in data and data["since_id"]:
			followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s AND user.id>%s AND user.id<%s ORDER BY user.name " + order + " LIMIT " + data["limit"] + ";",(data["user"], data["since"][0], data["since"][1], ))
		else:
			followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s ORDER BY user.name " + order + " LIMIT " + data["limit"] + ";",(data["user"], ))
	else:
		if "since_id" in data and data["since_id"]:
			followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s AND user.id>%s AND user.id<%s ORDER BY user.name " + order + ";",(data["user"], data["since"][0], data["since"][1], ))
		else:
			followersEmails = dbConnection.execQuery("SELECT email_follower FROM follow JOIN user ON follow.email_follower=user.email WHERE email_following=%s ORDER BY user.name " + order + ";",(data["user"]))
	followersEmails = sum(followersEmails,())
	followers = []
	dataRequest = {}
	dataRequest["related"] = []
	for followersEmail in followersEmails:
		dataRequest["user"] = followersEmail
		followers.append(api.dbOperations.user.details(dataRequest))
	return followers

def listFollowing(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	order = 'DESC'
	if "order" in data and data["order"]:
		order = data["order"]
	if "limit" in data and data["limit"]:
		if "since_id" in data and data["since_id"]:
			followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s AND user.id>%s AND user.id<%s ORDER BY user.name " + order + " LIMIT " + data["limit"] + ";",(data["user"], data["since"][0], data["since"][1], ))
		else:
			followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s ORDER BY user.name " + order + " LIMIT " + data["limit"] + ";",(data["user"], ))
	else:
		if "since_id" in data and data["since_id"]:
			followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s AND user.id>%s AND user.id<%s ORDER BY user.name " + order + ";",(data["user"], data["since"][0], data["since"][1], ))
		else:
			followingsEmails = dbConnection.execQuery("SELECT email_following FROM follow JOIN user ON follow.email_following=user.email WHERE email_follower=%s ORDER BY user.name " + order + ";",(data["user"], ))
	followingsEmails = sum(followingsEmails,())
	followings = []
	dataRequest = {}
	dataRequest["related"] = []
	for followingsEmail in followingsEmails:
		dataRequest["user"] = followingsEmail
		posts.append(api.dbOperations.user.details(dataRequest))
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
	if dbConnection.execQuery("SELECT * FROM follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"] )):
		dbConnection.execQuery("DELETE FROM follow WHERE email_follower = %s AND email_following = %s;",(data["follower"],data["followee"] ))
	else:
		raise Exception({"code":"INVALID REQUEST","message":"User with email '" + data["follower"] + "' doesn't follow user with email '" + data["followee"] + "'"})
	dataRequest={}
	dataRequest["user"] = data["follower"]
	return details(dataRequest)

def update(data):
	dbConnection.exists(entity="user", identificator="email", value=data["user"])
	dbConnection.execQuery("UPDATE user SET about=%s,name=%s WHERE email=%s;", (data["about"],data["name"],data["user"] ))
	dataRequest={}
	dataRequest["user"] = data["user"]
	return details(dataRequest)