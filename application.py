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


engine = create_engine(os.getenv("DATABASE_URL"))
db1 = scoped_session(sessionmaker(bind=engine))


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

@app.route("/input-<int:paper_id>",methods=['GET','POST'])
def input(paper_id):
    no_of_question=150
    if paper_id==25:
        no_of_question=200

    paper=Paper.query.filter_by(paper_id=paper_id).first()
    return render_template("inputanswer.html",paper=paper,no_of_question=no_of_question)

@app.route("/rank-<int:paper_id>",methods=['GET','POST'])
def rank(paper_id):
    marks=Marks.query.filter_by(paper_id=paper_id).order_by(Marks.provisonal_marks.desc()).all()
    paper=Paper.query.filter_by(paper_id=paper_id).first()
    noOfUser=db1.execute("select COUNT(provisonal_marks) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().count
    maxMark=db1.execute("select MAX(provisonal_marks) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().max
    minMark=db1.execute("select min(provisonal_marks) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().min
    avgMark=db1.execute("select CAST(AVG(provisonal_marks) AS DECIMAL(10,2)) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().avg
    #return render_template("rank.html",marks=marks,paper=paper,noOfUser=noOfUser,maxMark=maxMark,minMark=minMark,avgMark=avgMark)
    #we use mode=2 for only Rank
    return render_template("result.html",ranks=marks,paper=paper,noOfUser=noOfUser,maxMark=maxMark,minMark=minMark,avgMark=avgMark,mode=2)
@app.route("/calculate-<int:paper_id>",methods=['POST'])
def calculate(paper_id):
    rightQNo=[]
    wrongQNo=[]
    cancleQNO=[]
    eQNo=[]
    ans=[]
    right=0
    wrong=0
    e=0
    total=0
    cancle=0
    marks=0.0
    series=request.form.get("series")
    answer_email="admin"
    paper=Paper.query.filter_by(paper_id=paper_id).first()
    total_question=150
    if paper_id==25:
        total_question=200
    #answer=Answer.query().filter(and_(Answer.paper_id == paper_id,Answer.user_email=="admin",Answer.series==series)).first()

    answer=db1.execute("select * from answer_key WHERE paper_id=:paper_id AND  user_email=:answer_email AND series=:series",
    {"paper_id":paper_id,"answer_email":answer_email,"series":series}).fetchone()
    for qno in range(1,total_question+1):
        qstr='q'+str(qno)
        rightans1='T'
        if len(answer[qno+2])==1:
            rightans=answer[qno+2]  #first answer in 4th column
        else:
            rightans=answer[qno+2][0]
            rightans1=answer[qno+2][1]

        ans.append(request.form.get(qstr).upper())

        if rightans=='X':
            cancleQNO.append(total+1)
            cancle+=1

        elif ans[total]==rightans or ans[total]==rightans1:
            right+=1
            rightQNo.append(total+1)

        elif ans[total]=='E':
            e+=1
            eQNo.append(total+1)

        else:
            wrong+=1
            wrongQNo.append(total+1)
        total+=1

    marks= cancle*1 + right*1 - wrong*0.25
    user_email=request.form.get("useremail")
    fName=request.form.get("fName")
    lName=request.form.get("lName")
    mo=request.form.get("mo")
    newMark=Marks.query.filter(and_(Marks.email==user_email,Marks.paper_id==paper_id)).first()
    if(newMark):
        newMark.provisonal_marks=marks
        db.session.commit()
    else:
        addMark=Marks(paper_id=paper_id,email=user_email,firstName=fName,lastName=lName,provisonal_marks=marks,mobile=mo)
        db.session.add(addMark)
        db.session.commit()
    ranks=Marks.query.filter_by(paper_id=paper_id).order_by(Marks.provisonal_marks.desc()).all()
    noOfUser=db1.execute("select COUNT(provisonal_marks) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().count
    maxMark=db1.execute("select MAX(provisonal_marks) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().max
    minMark=db1.execute("select min(provisonal_marks) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().min
    avgMark=db1.execute("select CAST(AVG(provisonal_marks) AS DECIMAL(10,2)) FROM marks_details WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().avg
    return render_template("result.html",paper=paper,rightQNo=rightQNo,wrongQNo=wrongQNo,eQNo=eQNo,
    cancleQNO=cancleQNO,right=len(rightQNo),wrong=len(wrongQNo),e=e,cancle=cancle,total=total,marks=marks,
    noOfUser=noOfUser,maxMark=maxMark,minMark=minMark,avgMark=avgMark,mode=1,series=series,fName=fName,lName=lName,ranks=ranks)



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
    addMark=TestMarks(paper_id=paper_id,marks=marks)
    db.session.add(addMark)
    db.session.commit()
    ranks=TestMarks.query.filter_by(paper_id=paper_id).order_by(TestMarks.marks.desc()).all()
    noOfUser=db1.execute("select COUNT(marks) FROM test_marks WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().count
    maxMark=db1.execute("select MAX(marks) FROM test_marks WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().max
    minMark=db1.execute("select min(marks) FROM test_marks WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().min
    avgMark=db1.execute("select CAST(AVG(marks) AS DECIMAL(10,2)) FROM test_marks WHERE paper_id=:paper_id",{"paper_id":paper_id}).fetchone().avg
    #return render_template("result.html",paper=paper,rightQNo=rightQNo,wrongQNo=wrongQNo,eQNo=eQNo,right=len(rightQNo),wrong=len(wrongQNo),e=e,total=total,marks=marks,cancle=0)
    #we use mode=3 for test
    return render_template("result.html",paper=paper,rightQNo=rightQNo,wrongQNo=wrongQNo,eQNo=eQNo,right=len(rightQNo),wrong=len(wrongQNo),e=e,total=total,marks=marks,cancle=0,
                            noOfUser=noOfUser,maxMark=maxMark,minMark=minMark,avgMark=avgMark,mode=3,ranks=ranks)
@app.route("/module-<int:mode>",methods=['GET'])
def module(mode):
    if mode == 1 or mode == 2 :
        papers=Paper.query.filter_by(Test_Available=True).order_by(Paper.examdate.desc()).all()
        return render_template("paper.html",papers=papers,mode=mode)
    else:
        paperswithFKey=Paper.query.filter(and_(Paper.Key_Available==True,Paper.Key_Type==True)).order_by(Paper.examdate.desc()).all()
        paperswithPKey=Paper.query.filter(and_(Paper.Key_Available==True,Paper.Key_Type==False)).order_by(Paper.examdate.desc()).all()
        return render_template("paper.html",papers=paperswithFKey,mode=mode,papers2=paperswithPKey)

if __name__ == '__main__':
    app.debug = False
    app.secret_key = "9+3as4jj+nnqlu16xu49xag0i4-x(=6e$ljzsdcctkej1nil94"
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
