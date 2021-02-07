from get_info import collect_info
from flask import Flask, render_template, request

#db = collect_info('django')

app = Flask("RemoteJobs")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    global db
    job = request.args.get('search')
    if job in db:
        pass
    else:
        db[job] = collect_info(job)
    print(db)
    return render_template("jobs.html", num_jobs=len(db[job]), subject=job, jobs=db[job])


app.run(host="127.0.0.1")
