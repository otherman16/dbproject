import MySQLdb

host = "127.0.0.1"
user = "dbproject_user"
password = "dbproject_user"
db = "dbproject"

def execQuery(query, params):
	connection = None
	cursor = None
	try:
		connection = MySQLdb.connect(host,user,password,db)
		cursor = connection.cursor()
		cursor.execute(query, params)
		result = cursor.fetchall()
		connection.commit()
	except MySQLdb.Error as e:
		raise e
	finally:
		if connection:
			connection.close()
		if cursor:
			cursor.close()
	return result

def exists(entity, identiicator, value):
	if not len(execQuery('SELECT id FROM ' + entity + ' WHERE ' + identificator + ' = %s', (value, ))):
		raise Exception("No such element")
	return

def clear():
	execQuery("TRUNCATE forum",())