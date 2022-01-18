import base64
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, make_response, Blueprint
import time
from Visitor import Visitor, DataBase
from Admin import Admin
from random import shuffle

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Visitor.is_authorized() is not True:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@user.route('/', methods=("GET", "POST"))
def link_on_main():
    return redirect(url_for('user.home'))


@user.route('/statistics',  methods=("GET", "POST"))
@login_required
def statistics():
    results_tests = DataBase.get_history_user(Visitor.get_name())
    if results_tests.tests is not None:
        return render_template('user/statistics.html', user=Visitor, tests=results_tests.tests)
    else:
        return render_template('user/statistics.html', user=Visitor)


@user.route('/random_questions')
def home():
    list_questions = DataBase.get_questions()
    numbers = list(range(1, 39))
    shuffle(numbers)
    last_lst = []
    numbers = numbers[:5]
    for number in numbers:
        last_lst.append(list_questions[number])
    for one in last_lst:
        one.img = base64.b64encode(one.img).decode('ascii')
    return render_template('user/main.html', user=Visitor, questions=last_lst)


@user.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    elif request.method == 'POST':
        if Visitor.login(request):
            Visitor.remember_me(request.form['login'], request.form['password'])
            if Visitor.is_admin():
                return redirect(url_for('admin.home'))
            time.sleep(1)
            return redirect(url_for('home', user=Visitor))
        else:
            return redirect(url_for('user.login'))


@user.route('/sign-in', methods=("GET", "POST"))
def sign():
    if request.method == "GET":
        if not Visitor.is_authorized():# если пользователь не авторизован, идет на страницу авторизации
            response = make_response(render_template('user/sign-in.html', user=Visitor))
            return response
        else:# если пользователь авторизован, остается на этой же странице и выходит из текущего аккаунта
            Visitor.make_anonymous()
            return redirect(url_for('home', user=Visitor))
    elif request.method == "POST":
        if Visitor.register(request):
            Visitor.remember_me(request.form['username'], request.form['password'])
            time.sleep(1)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('user.sign'))


@user.route('/send', methods=("GET", "POST"))
def send():
    print(request.form['submit_button'])
    if Visitor.is_authorized():
        Visitor.save_results(int(request.form['submit_button']), 5)
    return redirect(url_for('home'))


@user.route('/questions_without_answers',  methods=("GET", "POST"))
@login_required
def only_questions():
    return render_template('user/questions.html', user=Visitor, themes=DataBase.get_themes(), images=get_refreshed_list_images())


def get_refreshed_list_images():
    all_themes_from_db = Admin.get_list_themes()
    all_images = []
    for theme in all_themes_from_db:
        all_images.append(base64.b64encode(theme.img).decode('ascii'))
    return all_images


@user.route('/test-from-theme', methods=("GET", "POST"))
def test_from_theme():
    theme = request.form['start_button']
    questions = DataBase.get_list_questions_from_theme(theme)
    counters = 0
    for question in questions:
        question.img = base64.b64encode(question.img).decode('ascii')
        counters += 1
    return render_template('user/test-from-theme.html', questions=questions,  user=Visitor, theme=theme, test_len=counters)
