from Visitor import Visitor
from DataBase import DataBase, Questions, Answers, Themes
import base64


class Admin(Visitor):
    @classmethod
    def get_refreshed_list_images(cls):
        all_themes_from_db = Admin.get_list_themes()
        all_images = []
        for theme in all_themes_from_db:
            all_images.append(base64.b64encode(theme.img).decode('ascii'))
        return all_images

    @classmethod
    def get_users_history(cls):
        return DataBase.get_users_history()

    @classmethod
    def get_history(cls):
        return DataBase.get_history()

    @classmethod
    def create_answer(cls, text, id_question, is_correct):
        new_answer = Answers(text=text, id_question=id_question, correct=is_correct)
        DataBase.load_object(new_answer)
        return new_answer.id

    @classmethod
    def create_question(cls, theme, text, image, mimetype):
        new_question = Questions(theme=theme, text=text, img=image, mimetype=mimetype)
        DataBase.load_object(new_question)
        return new_question.id

    @classmethod
    def create_theme(cls, theme, image, mimetype):
        new_theme = Themes(text=theme, img=image, mimetype=mimetype)
        DataBase.load_object(new_theme)
        return new_theme.id

    @classmethod
    def get_image_from_id(cls, id):
        return Questions.query.filter_by(id=id).first()

    @classmethod
    def get_counts_questions(cls):
        return DataBase.counts_record_questions()

    @classmethod
    def get_list_themes(cls):
        return DataBase.get_themes()

