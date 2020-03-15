from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient

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
                return "success"

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
        users.insert_one( { "_id":new_username, "username":new_username, "password":new_password, "posts": {} } )
    return render_template("register.html")

@app.route("/hub")
def hub():
    posts = []
    users_lst = users.find()
    for user in users_lst:
        for post in user["posts"]:
            posts.append(post)

    print(posts)
    return render_template("hub.html", posts=posts)


if __name__ == "__main__":
    #TODO: add ip number when hosting other computers
    app.run(debug=True, host="0.0.0.0")
