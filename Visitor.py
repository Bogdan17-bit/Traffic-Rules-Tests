from flask import session
from werkzeug.security import generate_password_hash
from DataBase import DataBase, Questions, Answers, Themes, Users
from datetime import datetime


class Visitor:
    @classmethod
    def test_is_pass(cls, number_correct, number_all_answers):
        if cls.percent_correct(number_correct, number_all_answers) >= 80:
            return True
        else:
            return False

    @classmethod
    def percent_correct(cls, number_correct, number_all_answers):
        return 100 / number_all_answers * number_correct

    @classmethod
    def save_results(cls, right_answers_number, number_all_answers):
        DataBase.create_and_save_field_in_history(user_name=cls.get_name(),
                                                  current_data=datetime.now().date(),
                                                  numbers=right_answers_number,
                                                  percent=cls.percent_correct(right_answers_number, number_all_answers),
                                                  test_is_pass=cls.test_is_pass(right_answers_number, number_all_answers))

    @classmethod
    def register(cls, exist_request):
        temp_user = cls.create_temp_user_from_sign(exist_request)
        if DataBase.is_registered(temp_user):
            return True
        else:
            return False

    @classmethod
    def login(cls, exist_request):
        temp_user = cls.create_temp_user_from_login(exist_request)
        if DataBase.is_authorized(temp_user):
            return True
        else:
            return False

    @classmethod
    def create_temp_user_from_sign(cls, exist_request):
        return Users(login=exist_request.form['username'], email=exist_request.form['email'], password=cls.get_hash(exist_request.form['password']))

    @classmethod
    def create_temp_user_from_login(cls, exist_request):
        return Users(login=exist_request.form['login'], email=exist_request.form['login'], password=exist_request.form['password'])

    @classmethod
    def get_hash(cls, user_password):
        return generate_password_hash(user_password, 'sha256')

    @classmethod
    def remember_me(cls, username, password):
        session['logged'] = 'True'
        session['user_name'] = username
        session['password'] = password

    @classmethod
    def make_anonymous(cls):
        session.pop('logged')
        session.pop('user_name')
        session.pop('password')

    @classmethod
    def is_admin(cls):
        if session.get('logged') == 'True':
            if session.get('user_name') == 'admin':
                return True

    @classmethod
    def is_authorized(cls):
        if session.get('logged') == 'True':
            return True
        else:
            return False

    @classmethod
    def get_name(cls):
        if session.get('logged'):
            return session.get('user_name')
        else:
            return 'Not authorized'
