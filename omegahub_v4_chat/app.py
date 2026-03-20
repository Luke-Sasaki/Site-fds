from flask import Flask, render_template, request, redirect, session
import sqlite3, os

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

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/login")
    con = db()
    msgs = con.execute("SELECT * FROM chat").fetchall()
    return render_template("chat.html", msgs=msgs, user=session["user"])

@app.route("/send", methods=["POST"])
def send():
    msg = request.form["msg"]
    user = session["user"]
    con = db()
    con.execute("INSERT INTO chat (user,msg) VALUES (?,?)",(user,msg))
    con.commit()
    return redirect("/chat")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
