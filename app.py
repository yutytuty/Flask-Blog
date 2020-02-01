from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")

db = client.Flask_Blog
users = db.users

@app.route()
def home():
    return render_template("home.html")
