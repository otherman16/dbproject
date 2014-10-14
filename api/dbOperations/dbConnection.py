import MySQLdb
import json
from django.http import HttpResponse

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
	except Exception as e
		raise Exception({"code":"UNKNOWN ERROR","message":str(e)})
	finally:
		if cursor:
			cursor.close()
		if connection:
			connection.close()
	return result

def exists(entity, identificator, value):
	if not len(execQuery('SELECT id FROM ' + entity + ' WHERE ' + identificator + ' = %s', (value, ))):
		raise Exception({"code":"NOT FOUND","message":"No such element in entity '" + entity + "' with '" + identificator + "'='" + value + "'"})

def notExists(entity, identificator, value):
	if not len(execQuery('SELECT id FROM ' + entity + ' WHERE ' + identificator + ' = %s', (value, ))):
		return True
	return False

def clear():
	execQuery("DELETE FROM follow",())
	execQuery("DELETE FROM post",())
	execQuery("DELETE FROM thread",())
	execQuery("DELETE FROM forum",())
	execQuery("DELETE FROM user",())

def recreateDatabase():
	connection = MySQLdb.connect('localhost','root','1')
	cursor = connection.cursor()
	cursor.execute("DROP DATABASE IF EXISTS dbproject")
	cursor.execute("CREATE DATABASE IF NOT EXISTS dbproject")
	cursor.execute("GRANT ALL ON dbproject.* TO 'dbproject_user'@'127.0.0.1'")
	connection.commit()
	cursor.close()
	connection.close()

def createTables():
	execQuery("CREATE TABLE IF NOT EXISTS user(" +
		"id INT(9) UNSIGNED NOT NULL AUTO_INCREMENT, " +
		"email VARCHAR(20) NOT NULL, " +
		"name VARCHAR(20) NOT NULL, " +
		"username VARCHAR(20) NOT NULL, " +
		"about VARCHAR(50) NOT NULL, " +
		"isAnonymous  BOOLEAN NOT NULL DEFAULT false, " +
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
		"FOREIGN KEY (user) REFERENCES user (email) ON UPDATE CASCADE ON DELETE CASCADE);",())
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
		"isClosed BOOLEAN NOT NULL DEFAULT false, " +
		"isDeleted BOOLEAN NOT NULL DEFAULT false, " +
		"PRIMARY KEY (id), " +
		"FOREIGN KEY (user) REFERENCES user (email) ON UPDATE CASCADE ON DELETE CASCADE, " +
		"FOREIGN KEY (forum) REFERENCES forum (short_name) ON UPDATE CASCADE ON DELETE CASCADE);",())
	execQuery("CREATE TABLE IF NOT EXISTS post(" +
		"id INT(9) UNSIGNED NOT NULL AUTO_INCREMENT, " +
		"message VARCHAR(150) NOT NULL, " +
		"forum VARCHAR(50) NOT NULL, " +
		"thread INT(9) UNSIGNED NOT NULL, " +
		"user VARCHAR(50) NOT NULL, " +
		"date DATETIME NOT NULL DEFAULT '2014-01-01 00:00:00', " +
		"dislikes INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"likes INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"parent INT(9) UNSIGNED DEFAULT NULL, " +
		"points INT(3) UNSIGNED NOT NULL DEFAULT 0, " +
		"isApproved BOOLEAN NOT NULL DEFAULT false, " +
		"isDeleted BOOLEAN NOT NULL DEFAULT false, " +
		"isEdited BOOLEAN NOT NULL DEFAULT false, " +
		"isHighlighted BOOLEAN NOT NULL DEFAULT false, " +
		"isSpam BOOLEAN NOT NULL DEFAULT false, " +
		"PRIMARY KEY (id), " +
		"FOREIGN KEY (user) REFERENCES user (email) ON UPDATE CASCADE ON DELETE CASCADE, " +
		"FOREIGN KEY (forum) REFERENCES forum (short_name) ON UPDATE CASCADE ON DELETE CASCADE, " +
		"FOREIGN KEY (thread) REFERENCES thread (id) ON UPDATE CASCADE ON DELETE CASCADE);",())

	execQuery("CREATE TABLE IF NOT EXISTS follow(" +
		"email_follower VARCHAR(20) NOT NULL, " +
		"email_following VARCHAR(20) NOT NULL, " +
		"UNIQUE KEY (email_follower,email_following), " +
		"FOREIGN KEY (email_follower) REFERENCES user (email) ON UPDATE CASCADE ON DELETE CASCADE, " +
		"FOREIGN KEY (email_following) REFERENCES user (email) ON UPDATE CASCADE ON DELETE CASCADE);",())

	execQuery("CREATE TABLE IF NOT EXISTS subscribe(" +
		"email_subscriber VARCHAR(20) NOT NULL, " +
		"id_subscribing INT(9) UNSIGNED NOT NULL, " +
		"UNIQUE KEY (email_subscriber,id_subscribing), " +
		"FOREIGN KEY (email_subscriber) REFERENCES user (email) ON UPDATE CASCADE ON DELETE CASCADE, " +
		"FOREIGN KEY (id_subscribing) REFERENCES thread (id) ON UPDATE CASCADE ON DELETE CASCADE);",())