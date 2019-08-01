import os

from flask import Flask,redirect,url_for,session,render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)


if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    return render_template("test1.html",questions=questions,paper=paper)

@app.route("/answer",methods=['GET'])
def answer():
    return render_template("takeanswer.html")


@app.route("/result-<int:paper_id>",methods=['POST'])
def result(paper_id):
    rightQNo=[]
    wrongQNo=[]
    eQNo=[]
    ans=[]
    right=0
    wrong=0
    e=0
    total=0
    marks=0.0
    paper=Paper.query.filter_by(paper_id=paper_id).first()
    questions=Question.query.filter_by(paper_id=paper_id).all()
    if paper_id!=6:
        for que in questions:
            ans.append(request.form.get("answer"+str(que.question_id)))
            if ans[total]==que.right_option:
                right+=1
                rightQNo.append(total+1)
            elif ans[total]=='E':
                e+=1
                eQNo.append(total+1)
            else:
                wrong+=1
                wrongQNo.append(total+1)
            total+=1
        marks= right*1 - wrong*0.25
    else:
        for que in questions:
            ans.append(request.form.get("answer"+str(que.question_id)))
            if ans[total]==que.right_option:
                if total<100:
                    right+=1
                else:
                    right+=0.5
                rightQNo.append(total+1)
            elif ans[total]=='E':
                e+=1
                eQNo.append(total+1)
            else:
                if total<100:
                    wrong+=1
                else:
                    wrong+=0.5
                wrongQNo.append(total+1)
            total+=1
        marks= right*1 - wrong*0.3
    return render_template("result.html",paper=paper,rightQNo=rightQNo,wrongQNo=wrongQNo,eQNo=eQNo,right=len(rightQNo),wrong=len(wrongQNo),e=e,total=total,marks=marks)

@app.route("/paper/<int:mode>",methods=['GET'])
def paper(mode):
    if mode != 3:
        papers=Paper.query.filter_by(Test_Available=True).order_by(Paper.examdate.desc()).all()
        return render_template("paper.html",papers=papers,mode=mode)
    else:
        papers=Paper.query.filter_by(Key_Available=True).order_by(Paper.examdate.desc()).all()
        return render_template("paper.html",papers=papers,mode=mode)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "9+3as4jj+nnqlu16xu49xag0i4-x(=6e$ljzsdcctkej1nil94"
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
