from flask import Flask, render_template, request
from models.models import TopoContent

# generate flask object
app=Flask(__name__)

# create the entrypoint "/"
@app.route("/")
def hello():
    return "Hello World"

# create the entrypoint "/index". return "index.html"
@app.route("/index")
def index():
    name = request.args.get("name")
    topos = TopoContent.query.all()
    return render_template("index.html", name = name, topos = topos)

@app.route("/index",methods=["post"])
def form():
    name = request.form["name"]
    return render_template("index.html", name = name)
if __name__ == "__main__":
    app.run(app = True)
