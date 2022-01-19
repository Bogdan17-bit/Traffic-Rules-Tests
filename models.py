from databases import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    tests = db.relationship('History', backref='users')


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    answers = db.relationship('Answers', backref='questions', lazy='subquery')
    theme = db.Column(db.String, nullable=False)


class Themes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    mimetype = db.Column(db.Text, nullable=True)
    img = db.Column(db.Text, nullable=True)


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    correct_answers_number = db.Column(db.Integer, nullable=False)
    correct_answers_percent = db.Column(db.Integer, nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.Date, nullable=False)
