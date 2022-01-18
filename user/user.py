import base64

from flask import Flask, render_template, request, redirect, url_for, make_response, Blueprint
import time
from Visitor import Visitor, DataBase
from random import shuffle

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')


@user.route('/')
def home():
    list_questions = DataBase.get_questions()
    numbers = list(range(1, 39))
    shuffle(numbers)
    last_lst = []
    numbers = numbers[:5]
    Visitor.save_numbers_questions(numbers)
    for number in numbers:
        print("random..." + str(number))
        print("normal object " + str(list_questions[number].id-1))
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
            return render_template(url_for('home', user=Visitor))
    elif request.method == "POST":
        if Visitor.register(request):
            Visitor.remember_me(request.form['username'], request.form['password'])
            time.sleep(1)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('user.sign'))


@user.route('/send', methods=("GET", "POST"))
def send():
    list_numbers_questions = Visitor.get_numbers_questions()
    print(list_numbers_questions)
    counter_right_answers = 0
    for current_number in list_numbers_questions:
        if request.form.get('group'+str(current_number)) == "True":
            counter_right_answers += 1
    print(counter_right_answers)
    return redirect(url_for('home'))
