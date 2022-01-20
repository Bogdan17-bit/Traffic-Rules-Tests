from flask import render_template, request
from flask import Blueprint, redirect, url_for
from Admin import Admin
from Visitor import Visitor
from functools import wraps

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Admin.is_authorized() is not True:
            return redirect(url_for('user.sign', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/upload', methods=['POST'])
@admin_required
def upload_new_question():
    picture = request.files['file']
    id_new_question = Admin.create_question(request.form.get('theme_selector'), request.form['question'], picture.read(), picture.mimetype)
    all_answers = request.form['first'], request.form['second'], request.form['third']
    variants = ['first', 'second', 'third']
    dict_variants = dict(zip(variants, all_answers))
    right_answer = request.form.get('group')
    for variant in dict_variants:
        if variant == right_answer:
            Admin.create_answer(dict_variants[variant], id_new_question, True)
        else:
            Admin.create_answer(dict_variants[variant], id_new_question, False)
    return render_template('admin/add.html', user=Admin, themes=Admin.get_list_themes(), length_list=len(Admin.get_list_themes()))


@admin.route('/create-theme', methods=['POST'])
@admin_required
def create_teme():
    picture = request.files['file']
    new_theme = request.form['theme']
    Admin.create_theme(new_theme, picture.read(), picture.mimetype)
    return render_template('admin/themes.html', user=Admin, themes=Admin.get_list_themes(), images=Admin.get_refreshed_list_images())


@admin.route('/')
@admin_required
def home():
    return redirect(url_for('admin.stats'))


@admin.route('/stats')
@admin_required
def stats():
    return render_template('admin/stats.html', user=Admin, users_history=Admin.get_users_history(), tests_number=len(Admin.get_history()))


@admin.route('/new_questions')
@admin_required
def new_questions():
    return render_template('admin/add.html', user=Admin, themes=Admin.get_list_themes(), length_list=len(Admin.get_list_themes()))


@admin.route('/themes')
@admin_required
def themes():
    return render_template('admin/themes.html', user=Admin, themes=Admin.get_list_themes(), images=Admin.get_refreshed_list_images())


@admin.route('/log-out', methods=("GET", "POST"))
def log_out():
    if request.method == "GET":
        Admin.make_anonymous()
        return redirect(url_for('home', user=Visitor))
