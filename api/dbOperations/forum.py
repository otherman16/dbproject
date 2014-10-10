from api.dbOperations import dbConnection

fields = ("id","name","short_name","user")

def create(name, short_name, user):
	dbConnection.exists(entity="user", identificator="email", value=user)
	forum = dbConnection.execQuery("SELECT id,name,short_name,user FROM forum WHERE short_name=%s",(short_name, ))
	return dict(zip(forum[0],fields))