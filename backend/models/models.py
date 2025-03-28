from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    qualification = db.Column(db.String)
    dob = db.Column(db.Date)
    role = db.Column(db.String, default='user')  # 'user' or 'admin'

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    total_marks = db.Column(db.Integer)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.String, nullable=False)
    question_type = db.Column(db.String, nullable=False)  # 'mcq', 'msq', 'numeric', 'text'
    options = db.Column(db.Text)  # JSON string for MCQ/MSQ options
    correct_answer = db.Column(db.Text, nullable=False)  # JSON string or raw answer depending on type

    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('results', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('results', lazy=True))
