from get_info import collect_info
from flask import Flask, render_template, request

db = collect_info()

app = Flask("RemoteJobs")


@app.route("/")
def home():
    return render_template("home.html")


app.run(host="127.0.0.1")
