from PIL import Image

from Lab3.task3.data import db_session
from Lab3.task3.data.users import User
db_session.global_init('db/users.db')
db_sess = db_session.create_session()
for user in db_sess.query(User).all():
    img = Image.open('static/photos/' + user.photo)
    width = 500
    height = 500
    resized_img = img.resize((width, height), Image.ANTIALIAS)
    resized_img.save('static/photos/' + user.photo)


















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
