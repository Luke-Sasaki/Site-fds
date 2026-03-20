import sqlite3
db = sqlite3.connect("database.db")

db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
db.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user TEXT, content TEXT)")
db.execute("CREATE TABLE chat (id INTEGER PRIMARY KEY, user TEXT, msg TEXT)")

db.commit()
db.close()
print("DB criada")
