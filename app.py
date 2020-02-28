from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")

db = client.Flask_Blog
users = db.users


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = data["password"]
        user = users.find_one( {"_id":username} )
        if user != None:
            if user["password"] == password:
                return "success"

            else:
                return "invalid username or passowrd"

        else:
            return "invalid username or password"

    return render_template("login.html")


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
    app.run(debug=True, host="0.0.0.0")
