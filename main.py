from get_info import collect_info
from flask import Flask, render_template, request

#db = collect_info('django')

app = Flask("RemoteJobs")
db = []


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    global db
    if len(db) != 0:
        db = []
    job = request.args.get('search')
    db = collect_info(job)

    return render_template("jobs.html", num_jobs=len(db), subject=job)


app.run(host="127.0.0.1")
