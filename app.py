from unicodedata import category
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_qrcode import QRcode
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import os
from dotenv import load_dotenv
import json
import json
import jyserver.Flask as jsf
import os,binascii

load_dotenv()

with open("config.json", "r") as json_file:
    config = json.load(json_file)

base_url = config["base_url"]

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["SECRET_KEY"] = "the random string"

db = SQLAlchemy(app)

@jsf.use(app)
class App:
    def __init__(self):
        pass

    def update(self, id):
        ids = id.split(".")
        data = str(self.js.document.getElementById(id).value)
        part = Part.query.filter_by(id=ids[0]).first()
        if ids[1] == "pn":
            part.pn = data
        elif ids[1] == "description":
            part.description = data
        elif ids[1] == "category":
            part.category = data
        elif ids[1] == "quantity":
            part.quantity = data
        elif ids[1] == "box":
            part.box = data
        db.session.commit()

    def delete_part(self, id):
        ids = id.split(".")
        data = str(self.js.document.getElementById(id).value)
        part = Part.query.filter_by(id=ids[0]).one()
        db.session.delete(part)
        print("deleting")
        db.session.commit()

class Part(db.Model):
    id = db.Column(db.String, primary_key=True)
    pn = db.Column(db.String)
    description = db.Column(db.String)
    category = db.Column(db.String)
    quantity = db.Column(db.String)
    box = db.Column(db.String)

    def __init__(
        self,
        pn: str,
        description: str,
        category: str,
        quantity: str,
        box: str
    ):
        self.id = str(binascii.b2a_hex(os.urandom(15)))[4:14]
        self.pn = pn
        self.description = description
        self.category = category
        self.quantity = quantity
        self.box = box


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        if request.form["pn"] != "" and request.form["description"] != "" and request.form["category"] and request.form["quantity"] != "" and request.form["box"] != "":
            part = Part(request.form["pn"], request.form["description"], request.form["category"], request.form["quantity"], request.form["box"])
            db.session.add(part)
            db.session.commit()
        else:
            print("Error")

    return App.render(render_template(
        "index.html",
        title="Home",
        cdns=["https://cdnjs.cloudflare.com/ajax/libs/d3/7.6.1/d3.min.js"],
        parts=Part.query.all()
    ))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="0.0.0.0")
