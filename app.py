import os.path
import sqlite3
import uuid

from PIL import Image
from flask import Flask, url_for, render_template, redirect, g, request, send_from_directory, flash, session
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from data.users import User
from data import db_session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from data.FDataBase import FDataBase

from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data.UserLogin import UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = '0cf1fa42fad749ab58c62063ddc5d4edb39c8ec5'

UPLOAD_FOLDER = 'static/photos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = 'db/menuUrl.db'
DEBUG = True
app.config.from_object(__name__)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    db = get_db('users', 'db/users.db')
    dbase = FDataBase(db)
    print('load user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def get_db(table, db):
    if not hasattr(g, 'menuUrl'):
        g.link_db = connect_db(db)
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'menuUrl'):
        g.link_db.close()


def main():
    app.run(port=8080, host='127.0.0.1')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    db = get_db('menuUrl', 'db/menuUrl.db')
    dbase = FDataBase(db)

    authorized = ""
    if 'id' in session:
        authorized = session['id']

    return render_template('base.html', menu=dbase.getMenu(), is_auth=authorized)


class LoginForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repPassword = PasswordField('Повторите пароль', validators=[DataRequired()])
    checkAdmin = PasswordField('Заполнить, если вы администратор')
    submit = SubmitField('Регистрация')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    db = get_db('menuUrl', 'db/menuUrl.db')
    dbase = FDataBase(db)
    db_for_users = get_db('users', 'db/users.db')
    dbase_for_users = FDataBase(db_for_users)
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase_for_users.GetUserByEmail(form.email.data)
        if user and check_password_hash(user['hashed_password'], form.password.data):
            userlogin = UserLogin()
            userlogin.create(user)
            session['id'] = userlogin.get_id()
            session['admin'] = userlogin.get_admin()
            login_user(userlogin)
            return redirect(url_for('index'))
        return redirect(url_for('index'))

    return render_template('login.html', title='Авторизация', menu=dbase.getMenu(), form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    print(session['id'])
    print(session['admin'])
    return redirect(url_for('login'))




@app.route('/register/', methods=['GET', 'POST'])
def register():
    db = get_db('menuUrl', 'db/menuUrl.db')
    dbase = FDataBase(db)

    authorized = ""
    if 'id' in session:
        authorized = session['id']

    db_session.global_init('db/users.db')
    emailError = ""
    codeAdmin = 'Admin'
    passwordRepeatError = ''
    form = RegisterForm()
    user = User()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user.name = form.username.data
        user.email = form.email.data
        user.age = form.age.data
        user.set_password(form.password.data)

        ## checking repeat password
        if form.password.data != form.repPassword.data:
            passwordRepeatError = 'Passwords do not match'
        ## checking of the existence of suh email in DB
        if db_sess.query(User.id).filter_by(email=form.email.data).scalar() is not None:
            emailError = 'This E-mail is already registered'
        ## checking admin
        if form.checkAdmin.data == codeAdmin:
            user.admin = True

        if emailError == '' and passwordRepeatError == '':
            file = request.files['photo']
            filename = secure_filename(file.filename)
            if file and allowed_file(filename):
                s = uuid.uuid4()
                user.photo = str(s) + '.jpg'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(s) + '.jpg'))
                ##resize photo 200 hight with save proportions
                img = Image.open('static/photos/' + user.photo)
                width = 64
                height = 64
                resized_img = img.resize((width, height), Image.ANTIALIAS)
                resized_img.save('static/photos/' + user.photo)
            db_sess.add(user)
            db_sess.commit()
            for user in db_sess.query(User).all():
                print(user)
            return redirect(url_for('user_display') + '?page=0')

    return render_template('register.html', title='Регистрация', emailError=emailError,
                           passwordRepeatError=passwordRepeatError, menu=dbase.getMenu(), form=form, is_auth=authorized)


@app.route('/users/')
def user_display():
    db_for_menu = get_db('menuUrl', 'db/menuUrl.db')
    dbase_for_menu = FDataBase(db_for_menu)
    db = get_db('users', 'db/users.db')
    dbase = FDataBase(db)
    authorized = ""
    if 'id' in session:
        authorized = session['id']

    curr_page = int(request.args.get('page'))
    pgcount = 1
    remainder = 0
    all_users = dbase.getAllUsers()
    for i in all_users:
        print(i[1])

    pgcount = len(all_users) // 4 + 1
    if pgcount == 0:
        pgcount = 1
    if curr_page > pgcount:
        abort(404)
    if pgcount % 4 > 0:
        remainder = len(all_users) % 4

    class pgstore:
        value = pgcount

    match curr_page:
        case 0:
            a = all_users[:4]
        case pgstore.value:
            a = all_users[pgcount - 1:remainder]
        case _:
            a = all_users[curr_page * 4:curr_page * 4 + 4]
    try:
        id_sess = session['_user_id']
    except:
        pass

    return render_template('users.html', users=a, curr_page=curr_page, pagecount=pgcount,
                           menu=dbase_for_menu.getMenu(), is_auth=authorized)


@app.route('/profile/<id>/', methods=['POST', 'GET'])
def user_profile(id=1):
    db_for_menu = get_db('menuUrl', 'db/menuUrl.db')
    dbase_for_menu = FDataBase(db_for_menu)
    db = get_db('users', 'db/users.db')
    dbase = FDataBase(db)
    userProfile = dbase.getUser(id)
    admin = ''
    if 'admin' in session:
        admin = session['admin']
    print(admin)

    if request.method == 'POST':
        dbase.updateUser(id, request.form.get('name'), request.form.get('email'), request.form.get('age'))
        db.commit()
        return redirect(url_for('user_profile', id=userProfile[0]))

    return render_template('profile.html', menu=dbase_for_menu.getMenu(), user=userProfile, auth=session['id'],
                           admin=admin)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    main()
