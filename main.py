from get_info import collect_info
from flask import Flask, render_template, request, send_file
from exporter import save_to_file

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
    job = job.lower()
    if job in db:
        pass
    else:
        db[job] = collect_info(job)
    return render_template("jobs.html", num_jobs=len(db[job]), subject=job, jobs=db[job])


@app.route("/export")
def export():
    try:
        job = request.args.get('search')
        if not job:
            raise Exception()
        job = job.lower()
        jobs = db[job]
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")


app.run(host="127.0.0.1")
