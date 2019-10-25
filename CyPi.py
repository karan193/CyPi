import sqlite3
import hashlib
import os

DB_NAME = "files.db"
PATH = "C:/Users/hooba/Desktop/CyPi/DB"
FILE_EXT = ".txt"

#checks the hash of the file automatically when show method is called or manually by user
def check_hash(title = None):
	if title == None:
		file_name = input("What is the name of the file? ")
		file_location = file_name + FILE_EXT
		
		hashcodes = []

		#reads the file that is being uploaded
		hasher = hashlib.md5()
		#opens the file as 'afile' in rb mode
		with open(file_location, 'rb') as afile:
			#reads the file to find hashcode
			contents = afile.read()
			print(contents)
			#updates the hashcode
			hasher.update(contents)
			#adds and prints the hashcode to the array
			hash = hasher.hexdigest()
			print(hash)
			hashcodes.append(hash)

		#connects to the database
		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()

		#finds the file in the database using the file title
		sqlite_fetch_blob = """SELECT * FROM 'files' WHERE title=?"""
		file_contents_db = cursor.execute(sqlite_fetch_blob,(file_name,))

		hasher_db = hashlib.md5()

		#reads the hashcode and appends it to the array
		contents_db = file_contents_db.fetchone()[2]
		print(contents_db)
		hasher_db.update(contents_db)
		hash = hasher_db.hexdigest()
		print(hash)
		hashcodes.append(hash)

		#
		if hashcodes[0] != hashcodes[1]:
			print("They are different. Panic.")
		else:
			print("They are the same file,")

		#closes connection to the database
		connection.close()
	else:
		file_name = title
		file_location = file_name + FILE_EXT
		
		hashcodes = []

		#reads the file that is being uploaded
		hasher = hashlib.md5()
		#opens the file as 'afile' in rb mode
		with open(file_location, 'rb') as afile:
			#reads the file to find hashcode
			contents = afile.read()
			#updates the hashcode
			hasher.update(contents)
			#adds and prints the hashcode to the array
			hash = hasher.hexdigest()
			hashcodes.append(hash)

		#connects to the database
		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()

		#finds the file in the database using the file title
		sqlite_fetch_blob = """SELECT * FROM 'files' WHERE title=?"""
		file_contents_db = cursor.execute(sqlite_fetch_blob,(file_name,))

		hasher_db = hashlib.md5()

		#reads the hashcode and appends it to the array
		contents_db = file_contents_db.fetchone()[2]
		hasher_db.update(contents_db)
		hash = hasher_db.hexdigest()
		hashcodes.append(hash)

		#returns if the files are the same or not
		return hashcodes[0] == hashcodes[1]

		#closes connection to the database
		connection.close()

def show():
	modified_files = []
	#connect to the database
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()

	#shows all files in the database
	sqlite_show = """SELECT * FROM 'files';"""

	cursor.execute(sqlite_show)
	
	#print all the rows
	rows = cursor.fetchall()
	for row in rows:
		#if file was modified, it will be appended to the modified files array and displayed to the user
		if not(check_hash(row[1])):
			modified_files.append(row[0])
		print(row)
	#if there was a modified file, the index of that file will be displayed to user
	if len(modified_files) > 0:
		print("files with the indices", modified_files, "were modified.")
	#close the connection
	connection.close()

#inserts all the files in the folder to the database
def insert_all():
	#connect to the database
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()

	#loop through the files in the directory
	for filename in os.listdir(PATH):
		#read the file data
		with open(PATH + '/' + filename, 'rb') as file:
			data = file.read()

		title = filename[:-4]

		#insert files with specified title and contents
		sqlite_insert_all = """INSERT INTO 'files'
						  ('title', 'contents') 
						  VALUES (?, ?);"""
		cursor.execute(sqlite_insert_all, (title, data))
		connection.commit()
		print(title, "inserted.")

	connection.close()

#inserts the file with the title and file user inputs
def insert(title, content):
	#connect to the database
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()
	
	#read the file data
	with open(content, 'rb') as file:
		data = file.read()

	#insert files with specified title and contents
	sqlite_insert = """INSERT INTO 'files'
					  ('title', 'contents') 
					  VALUES (?, ?);"""

	cursor.execute(sqlite_insert, (title, data))
	connection.commit()

	#close the connection
	connection.close()
	print(title, "inserted.")

#deletes the file depending on the title inputed
def delete(index):
	#connect to the database
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()

	#delete the files with the specified title
	sqlite_delete_with_param = """DELETE FROM 'files' WHERE id=?;"""

	cursor.execute(sqlite_delete_with_param, (index,))
	connection.commit()

	#close the connection
	connection.close()
	print("file with index", index, "deleted.")

#deletes all the files in the database
def delete_all():
	#connect to database
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()

	#delete all rows
	sqlite_delete_all = """DELETE FROM 'files';"""

	cursor.execute(sqlite_delete_all)
	connection.commit()

	#close the connection
	connection.close()
	print("All files deleted.")

#asks user what to do and does it (show, check hash, insert, insert all, delete, or delete all)
def main():
	action = input("What do you want to do with the database? (show, check hash, insert, insert all, delete, or delete all) ")
	if action.lower() == "check hash":
		check_hash()
	elif action.lower() == "show":
		show()
	elif action.lower() == "insert":
		how_many = int(input("How many files do you want to insert? "))
		for i in range(how_many):
			file_title = input("What is the title of the file? ")
			file_contents = input("What is the location of the file you want to insert? ")
			insert(file_title, file_contents)
	elif action.lower() == "delete":
		how_many = int(input("How many files do you want to delete? "))
		for i in range(how_many):
			file_index = input("What is the index of the file you want to delete? ")
			delete(file_index)
	elif action.lower() == "delete all":
		delete_all()
	elif action.lower() == "insert all":
		insert_all()
	else:
		print("I don't know that command")
	
if __name__ == "__main__":
	main()