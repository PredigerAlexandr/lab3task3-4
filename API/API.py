from flask import Flask, Blueprint
from flask_restful import Api, Resource
from Lab3.task3.data import db_session
from Lab3.task3.data.news import News
from Lab3.task3.data.categorys import Category
from Lab3.task3.data.news import get_categories


db_session.global_init('db/blogs.db')
db_sess = db_session.create_session()

API = Blueprint('api', __name__)
api = Api()
res_dic = {}

class post_collection(Resource):
    def get(self, category):
        if category == 'NONE':
            news = db_sess.query(News).all()
            for i in news:
                res_dic[i.id] = {"title": i.title, "content": i.content, "categories": get_categories(i.id)}
            return res_dic
        else:
            res_dic['cat'] = category
            post_category = db_sess.query(Category).filter(Category.name == category).first()
            for i in post_category.news:
                res_dic[i.id] = {"title":i.title, "content":i.content, "categories": get_categories(i.id)}
            return res_dic


api.add_resource(post_collection,'/api/post_by_category/<category>')