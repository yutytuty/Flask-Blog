from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import subprocess

app = Flask(__name__)

app.secret_key = b'\x9bBZe\xc7\xa3r\x18\x9d\xdd'

client = MongoClient("localhost", 27017)

db = client.Flask_Blog
users = db.users


@app.route("/")
@app.route("/home")
def home():
    username = "you are not logged in"
    if "username" in session:
        username = session["username"]
    return render_template("home.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = data["password"]
        user = users.find_one( {"_id":username} )
        if user != None:
            if user["password"] == password:
                session["username"] = username
                return redirect(url_for("post"))

            else:
                return "invalid username or passowrd"

        else:
            return "invalid username or password"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        new_username = data["username"]
        new_password = data["password"]
        if users.find({"_id":new_username}).count() == 0:
            users.insert_one( { "_id":new_username, "username":new_username, "password":new_password, "posts": [] } )
            return redirect(url_for("home"))

        return "Username already taken"

    return render_template("register.html")

@app.route("/hub")
def hub():
    posts = []
    users_lst = users.find()
    for user in users_lst:
        for post in user["posts"]:
            posts.append(post)

    return render_template("hub.html", posts=posts)

@app.route("/post", methods=["GET", "POST"])
def post():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        data = request.form
        title = data["title"]
        content = data["content"]
        author = session["username"]
        posts = users.find_one({"_id":author})["posts"]
        posts.append({"title":title, "author":author, "content":content})
        users.update_one({"_id":author}, {"$set":{"posts":posts}})
        return redirect("home")

    return render_template("post.html")


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        return redirect(url_for("home"))

    return redirect(url_for("home"))


if __name__ == "__main__":
    subprocess.Popen(["mongod"])
    app.run(debug=True, host="0.0.0.0")
