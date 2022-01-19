from models import *
from flask import flash
from werkzeug.security import check_password_hash


class DataBase:
    @classmethod
    def get_users_history(cls):
        return Users.query.all()

    @classmethod
    def get_history(cls):
        return History.query.all()

    @classmethod
    def get_list_questions_from_theme(cls, theme):
        return Questions.query.filter_by(theme=theme)

    @classmethod
    def get_history_user(cls, user_name):
        return Users.query.filter_by(login=user_name).first()

    @classmethod
    def get_themes(cls):
        return Themes.query.all()

    @classmethod
    def get_questions(cls):
        return Questions.query.all()

    @classmethod
    def create_and_save_field_in_history(cls, user_name, current_data, numbers, percent, test_is_pass):
        find_user = Users.query.filter_by(login=user_name).first()
        new_record = History(user_id=find_user.id, correct_answers_number=numbers, correct_answers_percent=percent, complete=test_is_pass, date=current_data)
        cls.load_object(new_record)

    @classmethod
    def is_authorized(cls, login_user):
        answer = cls.user_name_or_email_exist(login_user)
        if answer is not False:
            if cls.password_is_correct(login_user):
                return True
            else:
                flash("This password does not correct!", category='error')
                return False
        else:
            flash("This login/email does not exist!", category='error')
            return False

    @classmethod
    def is_registered(cls, sign_user):
        answer = cls.user_name_or_email_exist(sign_user)
        if answer is not False:
            flash(answer, category='error')
            return False
        else:
            if cls.user_is_add(sign_user):
                return True
            else:
                return False

    @classmethod
    def user_name_or_email_exist(cls, new_user):
        accounts = Users.query.all()
        for user in accounts:
            if user.login == new_user.login:
                return "This login is already exist!"
            if user.email == new_user.email:
                return "This email is already exist!"
        return False

    @classmethod
    def password_is_correct(cls, new_user):
        accounts = Users.query.all()
        for user in accounts:
            if user.login == new_user.login:
                if check_password_hash(user.password, new_user.password):
                    return True
                else:
                    return False

    @classmethod
    def user_is_add(cls, new_user):
        answer = cls.user_name_or_email_exist(new_user)
        try:
            if answer is False:
                db.session.add(new_user)
                cls.save()
                return True
        except:
            cls.roll_back()
            flash(answer, category='error')
            return False

    @classmethod
    def load_object(cls, db_object):
        db.session.add(db_object)
        cls.save()

    @classmethod
    def counts_record_questions(cls):
        return Questions.query.count()

    @classmethod
    def save(cls):
        db.session.flush()
        db.session.commit()

    @classmethod
    def roll_back(cls):
        db.session.rollback()
