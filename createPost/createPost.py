from flask import Blueprint, render_template, session, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from Lab3.task3.data.categorys import Category
from Lab3.task3.data.news import News

from Lab3.task3.data import db_session
from flask_wtf import FlaskForm

createPost = Blueprint('createPost', __name__, template_folder='templates', static_folder='static')


class PostForm(FlaskForm):
    title = StringField('Название статьи', validators=[DataRequired()])
    content = TextAreaField('Содержание статьи', validators=[DataRequired()])
    Business = BooleanField('Бизнесс')
    Economy = BooleanField('Экономика')
    Humor = BooleanField('Юмор')
    Politics = BooleanField('Политика')
    Education = BooleanField('Образование')
    submit = SubmitField('Добавить')

class UpdatePostForm(FlaskForm):
    title = StringField('Название статьи', validators=[DataRequired()])
    content = TextAreaField('Содержание статьи', validators=[DataRequired()])
    Business = BooleanField('Бизнесс')
    Economy = BooleanField('Экономика')
    Humor = BooleanField('Юмор')
    Politics = BooleanField('Политика')
    Education = BooleanField('Образование')
    submit = SubmitField('Сохранить')



@createPost.route('/', methods=['GET', 'POST'])
def index():
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    form = PostForm()
    news = News()
    if 'id' not in session:
        return abort(404)
    is_auth = session['id']

    if form.validate_on_submit():
        if 'id' not in session:
            return abort(404)
        news.user_id = session['id']
        news.title = form.title.data
        news.content = form.content.data
        if form.Business.data:
            cat = db_sess.query(Category).filter(Category.name == 'Business').first()
            news.categories.append(cat)

        if form.Economy.data:
            cat = db_sess.query(Category).filter(Category.name == 'Economy').first()
            news.categories.append(cat)

        if form.Humor.data:
            cat = db_sess.query(Category).filter(Category.name == 'Humor').first()
            news.categories.append(cat)

        if form.Politics.data:
            cat = db_sess.query(Category).filter(Category.name == 'Politics').first()
            news.categories.append(cat)

        if form.Education.data:
            cat = db_sess.query(Category).filter(Category.name == 'Education').first()
            news.categories.append(cat)

        db_sess.add(news)
        db_sess.commit()
        return redirect(url_for('index'))

    return render_template('createPost/create_post.html', form=form, title='Добавление статьи', is_auth=is_auth)


@createPost.route('/updatePost/<id_post>', methods=['GET', 'POST'])
def updatePost(id_post=0):
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    update_news = db_sess.query(News).filter(News.id==id_post).first()
    categories_news_name_list = []
    for i in update_news.categories:
        categories_news_name_list.append(i.name)
    print(categories_news_name_list)

    before_news = update_news
    form = UpdatePostForm()
    form.content.data = before_news.content
    for i in update_news.categories:
        print(i.name)
        if i.name == 'Business':
            form.Business.data==True
        if i.name == 'Economy':
            form.Economy.data==True
        if i.name == 'Business':
            form.Humor.data==True
        if i.name == 'Humor':
            form.Humor.data==True
        if i.name == 'Politics':
            form.Politics.data==True
        if i.name == 'Education':
            form.Education.data==True

    if 'id' not in session:
        print('дело дрянь')
        return abort(404)
    is_auth = session['id']
    print('дело дрянь')


    if id_post == 0:
        print('делодрянь3')
        abort(404)

    if form.validate_on_submit():
        update_news.title = form.title.data
        update_news.content = form.content.data
        update_news.categories.clear()

        if form.Business.data:
            cat = db_sess.query(Category).filter(Category.name == 'Business').first()
            update_news.categories.append(cat)

        if form.Economy.data:
            cat = db_sess.query(Category).filter(Category.name == 'Economy').first()
            update_news.categories.append(cat)

        if form.Humor.data:
            cat = db_sess.query(Category).filter(Category.name == 'Humor').first()
            update_news.categories.append(cat)

        if form.Politics.data:
            cat = db_sess.query(Category).filter(Category.name == 'Politics').first()
            update_news.categories.append(cat)

        if form.Education.data:
            cat = db_sess.query(Category).filter(Category.name == 'Education').first()
            update_news.categories.append(cat)

        print(update_news)
        db_sess.commit()
        return redirect(url_for('index'))




    return render_template('createPost/updatePost.html', form=form, title='Редктирование статьи', is_auth=is_auth,
                           now_news=before_news, categories_news=categories_news_name_list)


