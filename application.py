import os

from flask import Flask,redirect,url_for,session,render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)


if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/show/<int:paper_id>")
def show(paper_id):
    paper=Paper.query.filter_by(paper_id=paper_id).first()
    questions=Question.query.filter_by(paper_id=paper_id).all()
    return render_template("show.html",questions=questions,paper=paper)

@app.route("/test-<int:paper_id>")
def test(paper_id):
    paper=Paper.query.filter_by(paper_id=paper_id).first()
    questions=Question.query.filter_by(paper_id=paper_id).all()
    return render_template("test.html",questions=questions,paper=paper)

@app.route("/answer",methods=['GET'])
def answer():
    return render_template("takeanswer.html")

@app.route("/result",methods=['GET'])
def result():
    return render_template("result.html")

@app.route("/paper/<int:mode>",methods=['GET'])
def paper(mode):
    papers=Paper.query.all()
    return render_template("paper.html",papers=papers,mode=mode)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "9+3as4jj+nnqlu16xu49xag0i4-x(=6e$ljzsdcctkej1nil94"
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
