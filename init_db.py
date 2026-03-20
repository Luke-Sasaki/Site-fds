import sqlite3
db = sqlite3.connect("database.db")

db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
db.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, user TEXT, content TEXT)")
db.execute("CREATE TABLE likes (id INTEGER PRIMARY KEY, post_id INTEGER)")
db.execute("CREATE TABLE comments (id INTEGER PRIMARY KEY, post_id INTEGER, user TEXT, comment TEXT)")

db.commit()
db.close()
print("DB criada")
