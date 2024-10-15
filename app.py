from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from translateCN_ENG import translate_zh_to_en, translate_en_to_zh
from filter import filter
from gen_report import gen_report

app = Flask(__name__)

connection = MongoClient("mongodb://localhost:27017/")
db = connection["admin"]
feedbacks = db.feedbacks


@app.route("/")
def home():
    message = request.args.get("message", "")
    return render_template("write.html", message = message)

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    feedback = request.form.to_dict()
    print(feedback)
    feedback['feedback']= translate_zh_to_en(feedback['feedback'])
    if(filter(feedback['feedback'])):
        feedbacks.insert_one(feedback)
        message = "成功提交 Submitted Successfully"
    else:
        message = "反饋未能成功識別 Could Not Detect Valid Feedback"
    return redirect(url_for("home", message=message))

@app.route("/report")
def report():
    message = request.args.get("message", "")
    title = request.args.get("title", "")
    return render_template("report.html", title = title, message = message)

@app.route("/generate", methods=["POST"])
def generate():
    filter = request.form.to_dict()
    query = []
    for key, value in filter.items():
        if value == "all":
            continue
        query.append({str(key): str(value)})
        print(query)
    cursor = feedbacks.find({
        "$and": query
    })
    payload = ""
    for document in cursor:
        payload += str(document['feedback'])
    message = gen_report(payload)
    return redirect(url_for("report", title="關於此群體之報告 Summative Report of This Particular Group" ,message=message))