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
        return render_template('user/statistics.html', user=Visitor, tests=results_tests.tests, number_results_find=len(results_tests.tests))
    else:
        return render_template('user/statistics.html', user=Visitor, number_results_find=0)


@user.route('/random_questions', methods=("GET", "POST"))
def home():
    if request.method == 'GET':
        list_questions = DataBase.get_questions()
        numbers = list(range(0, 39))
        shuffle(numbers)
        last_lst = []
        numbers = numbers[:5]
        for number in numbers:
            last_lst.append(list_questions[number])
        for one in last_lst:
            if isinstance(one.img, str) is False:
                one.img = base64.b64encode(one.img).decode('ascii')
        return render_template('user/main.html', user=Visitor, questions=last_lst)
    elif request.method == 'POST':
        list_questions = DataBase.get_questions()
        numbers = list(range(1, 39))
        shuffle(numbers)
        last_lst = []
        numbers = numbers[:5]
        for number in numbers:
            last_lst.append(list_questions[number])
        for one in last_lst:
            if isinstance(one.img, str) is False:
                one.img = base64.b64encode(one.img).decode('ascii')
        print('IT MY FUCKING SUBMIT BUTTON VALUE')
        print(request.form.get('submit_button'))
        if Visitor.is_authorized():
            Visitor.save_results(int(request.form['submit_button']), 5)
        if Visitor.test_is_pass(int(request.form['submit_button']), 5):
            return render_template('user/main.html', user=Visitor, questions=last_lst, test_is_pass='True')
        else:
            return render_template('user/main.html', user=Visitor, questions=last_lst, test_is_pass='False')


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
    if request.method == 'GET':
        return render_template('user/questions.html', user=Visitor, themes=DataBase.get_themes(), images=get_refreshed_list_images_for_themes())
    elif request.method == 'POST':
        if request.form.get('submit_button'):
            all_themes = DataBase.get_themes()
            test_is_pass = 'False'
            if Visitor.test_is_pass(int(request.form['submit_button']), 5):
                test_is_pass = 'True'
            return render_template('user/questions.html', user=Visitor, themes=all_themes, test_is_pass=test_is_pass, images=get_refreshed_list_images_for_themes())


def get_refreshed_list_images_for_themes():
    all_themes_from_db = Admin.get_list_themes()
    all_images = []
    for theme in all_themes_from_db:
        all_images.append(base64.b64encode(theme.img).decode('ascii'))
    return all_images


@user.route('/test-from-theme', methods=("GET", "POST"))
def test_from_theme():
    if request.method == 'POST':
        if request.form.get('start_button'):
            theme = request.form['start_button']
            questions = DataBase.get_list_questions_from_theme(theme)
            counter = 0
            for question in questions:
                if isinstance(question.img, str) is False:
                    question.img = base64.b64encode(question.img).decode('ascii')
                counter += 1
            return render_template('user/test-from-theme.html', user=Visitor, questions=questions, theme=theme, test_len=counter)
