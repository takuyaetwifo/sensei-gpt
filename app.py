
from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        con.close()
        if row:
            session["user_id"] = row[0]
            session["username"] = username
            session["role"] = row[1]
            return redirect("/chat")
        else:
            error = "ユーザー名またはパスワードが違います"
    return render_template("login.html", error=error)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user_id" not in session:
        return redirect("/login")
    username = session.get("username", "ゲスト")
    return render_template("chat.html", username=username)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/admin/history")
def admin_history():
    if session.get("role") != "admin":
        return "アクセスできません", 403
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute("SELECT user_id, user_input, gpt_response, timestamp FROM chatlog ORDER BY timestamp DESC")
    rows = cur.fetchall()
    con.close()
    return render_template("admin_history.html", rows=rows, admin=session.get("username"))
