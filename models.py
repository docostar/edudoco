from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
from sqlalchemy import Column, Integer,DateTime,String,ForeignKey,Boolean
db = SQLAlchemy()

class Paper(db.Model):
    __tablename__ = "paper"
    paper_id = db.Column(db.Integer, primary_key=True)
    examname = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    series = db.Column(db.String)
    exambody = db.Column(db.Integer, nullable=False)
    examdate=db.Column(db.DateTime, nullable=False) #default=datetime.datetime.utcnow)
    Key_Available=db.Column(db.Boolean, nullable=False)
    Test_Available=db.Column(db.Boolean, nullable=False)

class Question(db.Model):
    __tablename__ = "question"
    paper_id = Column(Integer,ForeignKey("paper.paper_id"), nullable=False)
    question_id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    right_option=Column(String,nullable=False)
    difflevel=Column(db.SMALLINT)
    explanation = Column(String)

class User(db.Model):
    __tablename__ = "user_info"
    email = Column(String, primary_key=True)
    fName = Column(String, nullable=False)
    lName = Column(String, nullable=False)
    mo = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Answer(db.Model):
    __tablename__ = "answer_key"
    paper_id = Column(Integer,ForeignKey("paper.paper_id"), nullable=False)
    user_email = Column(String,ForeignKey(".user_info.emil"), nullable=False)
    series=Column(String, nullable=False)
