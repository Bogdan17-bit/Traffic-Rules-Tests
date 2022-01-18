from flask import Flask, redirect, url_for

from admin.admin import admin
from user.user import user
from databases import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '4d5w2b9t5z1q4f5vd4w5vd2h3x5zq7q7q7q8'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

app.register_blueprint(user, url_prefix='/home')
app.register_blueprint(admin, url_prefix='/admin')

db.init_app(app)


@app.route('/')
def home():
    return redirect(url_for('user.home'))


if __name__ == '__main__':
    app.run(debug=True)

