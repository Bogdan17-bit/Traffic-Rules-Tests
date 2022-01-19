import base64

from flask import render_template, request, Response
from flask import Blueprint, redirect, url_for
from Admin import Admin

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin.route('/upload', methods=['POST'])
def upload_new_question():
    picture = request.files['file']
    id_new_question = Admin.create_question(request.form.get('theme_selector'), request.form['question'], picture.read(), picture.mimetype)

    all_answers = request.form['first'], request.form['second'], request.form['third']
    variants = ['first', 'second', 'third']
    dict_variants = dict(zip(variants, all_answers))
    print(dict_variants)
    right_answer = request.form.get('group')
    print(right_answer)
    for variant in dict_variants:
        if variant == right_answer:
            Admin.create_answer(dict_variants[variant], id_new_question, True)
        else:
            Admin.create_answer(dict_variants[variant], id_new_question, False)
    return render_template('admin/add.html', user=Admin, themes=Admin.get_list_themes(), length_list=len(Admin.get_list_themes()))


@admin.route('/create-theme', methods=['POST'])
def create_teme():
    picture = request.files['file']
    new_theme = request.form['theme']
    Admin.create_theme(new_theme, picture.read(), picture.mimetype)
    return render_template('admin/themes.html', user=Admin, themes=Admin.get_list_themes(), images=get_refreshed_list_images())


def get_refreshed_list_images():
    all_themes_from_db = Admin.get_list_themes()
    all_images = []
    for theme in all_themes_from_db:
        all_images.append(base64.b64encode(theme.img).decode('ascii'))
    return all_images


@admin.route('/images/<int:image_id>')
def display_image(image_id):
    img = Admin.get_image_from_id(image_id)
    if not img:
        return "Not exist!", 404
    return Response(img.img, mimetype=img.mimetype)


@admin.route('/')
def home():
    return redirect(url_for('admin.stats'))


@admin.route('/stats')
def stats():
    return render_template('admin/stats.html', user=Admin, users_history=Admin.get_users_history(), tests_number=len(Admin.get_history()))


@admin.route('/new_questions')
def new_questions():
    return render_template('admin/add.html', user=Admin, themes=Admin.get_list_themes(), length_list=len(Admin.get_list_themes()))


@admin.route('/themes')
def themes():
    return render_template('admin/themes.html', user=Admin, themes=Admin.get_list_themes(), images=get_refreshed_list_images())
