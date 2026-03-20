from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo"

def db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    con = db()
    posts = con.execute("SELECT * FROM posts").fetchall()
    return render_template("index.html", posts=posts, user=session["user"])

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        u = request.form["username"]
        p = request.form["password"]
        con = db()
        con.execute("INSERT INTO users (username,password) VALUES (?,?)",(u,p))
        con.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u = request.form["username"]
        p = request.form["password"]
        con = db()
        data = con.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone()
        if data:
            session["user"]=u
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/post", methods=["POST"])
def post():
    content = request.form["content"]
    user = session["user"]
    con = db()
    con.execute("INSERT INTO posts (user,content) VALUES (?,?)",(user,content))
    con.commit()
    return redirect("/")

@app.route("/like/<int:id>")
def like(id):
    con = db()
    con.execute("INSERT INTO likes (post_id) VALUES (?)",(id,))
    con.commit()
    return redirect("/")

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    user = session["user"]
    c = request.form["comment"]
    con = db()
    con.execute("INSERT INTO comments (post_id,user,comment) VALUES (?,?,?)",(id,user,c))
    con.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
