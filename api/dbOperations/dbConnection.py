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
	except Exception as e:
		raise e
	finally:
		if connection:
			connection.close()
		if cursor:
			cursor.close()
	return result

def exists(entity, identificator, value):
	if not len(execQuery('SELECT id FROM ' + entity + ' WHERE ' + identificator + ' = %s', (value, ))):
		raise Exception("No such element in entity '" + entity + "' with '" + identificator + "'='" + value + "'")
		return False
	return True

def clear():
	execQuery("TRUNCATE forum",())

def dropTables():
	execQuery("DROP TABLE IF EXISTS forum;",())
	execQuery("DROP TABLE IF EXISTS post;",())
	execQuery("DROP TABLE IF EXISTS user;",())
	execQuery("DROP TABLE IF EXISTS thread;",())
	execQuery("DROP TABLE IF EXISTS follow;",())

def createTables():
	execQuery("CREATE TABLE IF NOT EXISTS user(" +
		"id INT(9) UNSIGNED NOT NULL AUTO_INCREMENT, " +
		"email VARCHAR(20) NOT NULL, " +
		"name VARCHAR(20) NOT NULL, " +
		"username VARCHAR(20) NOT NULL, " +
		"about VARCHAR(50) NOT NULL, " +
		"isAnonymous TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"PRIMARY KEY (email), " +
		"UNIQUE KEY (id));",())
	execQuery("CREATE TABLE IF NOT EXISTS forum(" + 
		"id INT(9) UNSIGNED NOT NULL AUTO_INCREMENT, " +
		"name VARCHAR(150) NOT NULL, " +
		"short_name VARCHAR(50) NOT NULL, " +
		"user VARCHAR(20) NOT NULL, " +
		"PRIMARY KEY (short_name), " +
		"UNIQUE KEY (name), " +
		"UNIQUE KEY (id), " +
		"FOREIGN KEY (user) REFERENCES user (email));",())
	execQuery("CREATE TABLE IF NOT EXISTS post(" +
		"id INT(9) UNSIGNED NOT NULL AUTO_INCREMENT, " +
		"message VARCHAR(150) NOT NULL, " +
		"forum VARCHAR(50) NOT NULL, " +
		"thread VARCHAR(50) NOT NULL, " +
		"date DATETIME NOT NULL DEFAULT '2014-01-01 00:00:00', " +
		"dislikes INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"likes INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"parent INT(9) UNSIGNED, " +
		"points INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"thread INT(9) UNSIGNED NOT NULL, " +
		"isApproved TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"isDeleted TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"isEdited TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"isHighlighted TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"isSpam TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"PRIMARY KEY (id), " +
		"FOREIGN KEY (forum) REFERENCES forum (short_name), " +
		"FOREIGN KEY (thread) REFERENCES thread (slug));",())
	execQuery("CREATE TABLE IF NOT EXISTS thread(" +
		"id INT(9) UNSIGNED NOT NULL AUTO_INCREMENT, " +
		"title VARCHAR(50) NOT NULL, " +
		"slug VARCHAR(50) NOT NULL, " +
		"message VARCHAR(50) NOT NULL, " +
		"user VARCHAR(50) NOT NULL, " +
		"forum VARCHAR(50) NOT NULL, " +
		"date DATETIME NOT NULL DEFAULT '2014-01-01 00:00:00', " +
		"likes INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"dislikes INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"points INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"posts INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"isClosed TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"isDeleted TINYINT(1) UNSIGNED NOT NULL DEFAULT 0, " +
		"PRIMARY KEY (id), " +
		"FOREIGN KEY (user) REFERENCES user (email), " +
		"FOREIGN KEY (forum) REFERENCES forum (short_name));",())

	execQuery("CREATE TABLE IF NOT EXISTS follow(" +
		"id_follower INT(9) UNSIGNED NOT NULL, " +
		"id_following INT(9) UNSIGNED NOT NULL, " +
		"UNIQUE KEY (id_follower,id_following));",())