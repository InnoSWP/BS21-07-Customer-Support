# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, jsonify, redirect
import json
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")
link = "https://api.telegram.org/bot5505131588:AAF_LojeoLfIAlhd6UJnV36gDS-yDZei9Nw/sendMessage"
app.secret_key = "FKJSADHFASHDLBSFJHFVJKHLSDFBHZDC,H"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main"
app.config["SQLALCHEMY_BINDS"] = {
    'users': 'sqlite:///users.db',
    'instances': 'sqlite:///instances.db',
    'busies': 'sqlite:///busies.db'
}

db = SQLAlchemy(app)
prev = 0
history = {}
query = []


class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Instance(db.Model):
    __bind_key__ = 'instances'
    number = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Instance %r>' % self.number


class Busy(db.Model):
    __bind_key__ = 'busies'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Busy %r>' % self.id


def send_all_request(number, text):
    if Instance.query.filter_by(number=number).first() is not None:
        if text == "close":
            inst = Instance.query.filter_by(number=number).first()
            id = inst.id
            busy = Busy.query.filter_by(id=id).first()
            busy.number = 0
            db.session.delete(inst)
            db.session.commit()
            data = {}
            data["chat_id"] = id
            data["text"] = "Request closed!"
            requests.post(url=link, data=data)
        else:
            inst = Instance.query.filter_by(number=number).first()
            id = inst.id
            data = {}
            data["chat_id"] = id
            data["text"] = text
            requests.post(url=link, data=data)
    else:
        keyboard = json.dumps({
            "inline_keyboard": [
                [
                    {"text": "Start", "callback_data": f'open==={number}==={text}'},
                ]
            ]
        })
        for i in User.query.all():
            # print(i.role, Busy.query.filter_by(id=i.id).first().number)
            if i.role == "user" and Busy.query.filter_by(id=i.id).first().number == 0:
                data = {}
                data['chat_id'] = i.id
                data['text'] = f"New request № {number}"
                data['reply_markup'] = keyboard
                print(data)
                requests.post(url=link, data=data)
                # await bot.send_message(i[0], f"New request № {number}", reply_markup=inline_kb1)


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
    return "OK"


@app.route("/get")
def get():
    global query
    return jsonify(query)


@app.route("/get_user", methods=["GET", "POST"])
def get_user():
    global query
    query.append({"id": int(request.args.get("id")), "type": "user", "text": request.args.get("text")})
    send_all_request(number=int(request.args.get("id")), text=request.args.get("text"))
    return "OK"


@app.route("/quit")
def quit():
    send_all_request(session['request_id'], "close")
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
