
from flask import Flask, request, render_template, redirect, url_for, session
from models import db, User, ChatLog
from config import Config
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="ログイン失敗")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]
        gpt_response = f"（仮）{user_input}に対する返答"
        log = ChatLog(user_id=session["user_id"], user_input=user_input, gpt_response=gpt_response, timestamp=datetime.now())
        db.session.add(log)
        db.session.commit()
    rows = ChatLog.query.filter_by(user_id=session["user_id"]).order_by(ChatLog.id.desc()).limit(10).all()
    return render_template("chat.html", username=session["username"], rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
