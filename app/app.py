from flask import Flask, render_template, request
from models.models import TopoContent
from models.database import db_session
from datetime import datetime

# generate flask object
app=Flask(__name__)

# create the entrypoint "/index". return "index.html"
@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name")
    topos = TopoContent.query.all()
    return render_template("index.html", name = name, topos = topos)

@app.route("/index",methods=["post"])
def form():
    name = request.form["name"]
    topos = TopoContent.query.all()
    return render_template("index.html", name = name, topos = topos)

# レコードの追加
@app.route("/add", methods=["post"])
def recordAdd():
    title = request.form["title"]
    body = request.form["body"]
    content = TopoContent(title=title, body=body,date=datetime.now())
    db_session.add(content)
    db_session.commit()
    return index()

# レコードの削除
@app.route("/delete", methods=["post"])
def recordDel():
    idLists = request.form.getlist("delete")
    for id in idLists:
        content = TopoContent.query.filter_by(id = id).first()
        db_session.delete(content)
    db_session.commit()
    return index()

@app.route("/update", methods=["post"])
def recordUpdate():
    id = request.form.get("update")
    content = TopoContent.query.filter_by(id = id).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return index()

if __name__ == "__main__":
    app.run(app = True)
