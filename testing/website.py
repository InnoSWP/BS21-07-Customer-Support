# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, jsonify, redirect
import requests

app = Flask(__name__)
app.secret_key = "FKJSADHFASHDLBSFJHFVJKHLSDFBHZDC,H"
prev = 0
history = {}
query = []


@app.route("/")
def hello():
    global prev, history
    if "request_id" not in session:
        session["request_id"] = prev + 1
        history[prev + 1] = []
        prev += 1
    print(session["request_id"])
    return render_template("index.html", session_id=session["request_id"])


@app.route("/send/<id>/<text>", methods=['GET', 'POST'])
def send(id, text):
    query.append({"id": id, "text": text, "type": "bot"})
    print (text)
    requests.get("https://api.telegram.org/bot5496927593:AAHwWb5vh_XJbeisVKakfDj92wkgloqf6Yw/sendMessage?chat_id=-764558607&text=/start @swp_g7_bs21_backend_bot")
    # requests.get("https://api.telegram.org/bot5496927593:AAHwWb5vh_XJbeisVKakfDj92wkgloqf6Yw/sendMessage?chat_id=-764558607&text=" + text)
    return "OK"


@app.route("/get")
def get():
    global query
    return jsonify(query)


@app.route("/get_user", methods=["GET", "POST"])
def get_user():
    global query
    query.append({"id" : int(request.args.get("id")), "type" : "user", "text" : request.args.get("text")})
    return "OK"


@app.route("/quit")
def quit():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
