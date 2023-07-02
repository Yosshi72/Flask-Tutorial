from flask import Flask, render_template, request, session, redirect, url_for
from models.models import TopoContent, User
from models.database import db_session
from datetime import datetime
from hashlib import sha256
from app import key

# generate flask object
app=Flask(__name__)
app.secret_key = key.SECRET_KEY

@app.route("/")
def init():
    return redirect(url_for("top"))

# create the entrypoint "/index". return "index.html"
@app.route("/index")
def index():
    if "user_name" in session:
        name = request.args.get("name")
        topos = TopoContent.query.all()
        return render_template("index.html", name = name, topos = topos)
    else:
        redirect(url_for("/index"), status = "logout")

# レコードの追加
@app.route("/add", methods=["post"])
def recordAdd():
    title = request.form["title"]
    body = request.form["body"]
    content = TopoContent(title=title, body=body,date=datetime.now())
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index"))

# レコードの削除
@app.route("/delete", methods=["post"])
def recordDel():
    idLists = request.form.getlist("delete")
    for id in idLists:
        content = TopoContent.query.filter_by(id = id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/update", methods=["post"])
def recordUpdate():
    id = request.form.get("update")
    content = TopoContent.query.filter_by(id = id).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return redirect(url_for("index"))

@app.route("/login", methods=["post"])
def login():
    # formで記入したユーザネームを受け取り，DBにあるか確認
    user_name = request.form["user_name"]
    user =User.query.filter_by(user_name = user_name).first()

    if user:
        # formで記入したパスワードをkey.pyにあるSALTでハッシュ化する
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        # DBに登録されたパスワードとformのパスワードが一致するか
        if user.hashed_passwd == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top", status = "wrong password"))
    else:
        return redirect(url_for("top", status = "not found"))

@app.route("/registar", methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user =User.query.filter_by(user_name = user_name).first()

    if user:
        return redirect(url_for("newcomer", status = "existed"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name = user_name, hashed_passwd = hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top", status = "logout"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html", status = status)

@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html", status = status)

if __name__ == "__main__":
    app.run(app = True)
