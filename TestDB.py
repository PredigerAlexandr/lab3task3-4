from PIL import Image

from Lab3.task3.data import db_session, news
from Lab3.task3.data.users import User
from Lab3.task3.data.news import News
# from Lab3.task3.data import news
from Lab3.task3.data.categorys import Category

db_session.global_init('db/blogs.db')
db_sess = db_session.create_session()
# news = News()
# news.title = 'Князь'
# news.content = 'Князь хороший был2'
# news.user_id = 2
# cat = db_sess.query(Category).filter(Category.id == 1).first()
# print(cat.name)
# news.categories.append(cat)
# cat = db_sess.query(Category).filter(Category.id == 2).first()
# news.categories.append(cat)
# db_sess.add(news)
# db_sess.commit()

# news = db_sess.query(News).filter(News.id==12).first()
# print(news.categories[1].name)

# update_news = db_sess.query(News).filter(News.id==1).first()
# update_news.title = "12312231223qrergwergfergqaerdsfdsfsfsdfsdfsfsf"
#
# db_sess.commit()
# io = []
# if any(x in io for x in news.get_categories(1)):
#     print("!")
# user = db_sess.query(User).filter(User.id==1).first()
# post_list = user.news
# for i in post_list:
#     print(i.title)
# newss = db_sess.query(News).filter(News.id==1).first()
# print(news.get_categories(newss.id))
category = db_sess.query(Category).filter(Category.name=='Business').first()
print((category.news).json())



















# import os.path
# import sqlite3
# import uuid
#
# from flask import Flask, url_for, render_template, redirect, g, request, send_from_directory, flash
# from werkzeug.utils import secure_filename
#
# from data.users import User
# from data import db_session
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField
# from wtforms.validators import DataRequired, Email
# from data.FDataBase import FDataBase
#
# app = Flask(__name__)
#
# UPLOAD_FOLDER = 'static/photos'
# # расширения файлов, которые разрешено загружать
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# def main():
#     app.run(port=8080, host='127.0.0.1')
#
#
# def allowed_file(filename):
#     """ Функция проверки расширения файла """
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # проверим, передается ли в запросе файл
#         if 'file' not in request.files:
#             # После перенаправления на страницу загрузки
#             # покажем сообщение пользователю
#             flash('Не могу прочитать файл')
#             return redirect(request.url)
#         file = request.files['file']
#         # Если файл не выбран, то браузер может
#         # отправить пустой файл без имени.
#         if file.filename == '':
#             flash('Нет выбранного файла')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             # безопасно извлекаем оригинальное имя файла
#             filename = secure_filename(file.filename)
#             # сохраняем файл
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # если все прошло успешно, то перенаправляем
#             # на функцию-представление `download_file`
#             # для скачивания файла
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Загрузить новый файл</title>
#     <h1>Загрузить новый файл</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     </html>
#     '''
#
#
# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)
#
#
# if __name__ == '__main__':
#     main()
