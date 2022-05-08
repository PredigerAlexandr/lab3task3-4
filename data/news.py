import datetime

import sqlalchemy

from . import db_session
from .categorys import news_category
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DATE, default=datetime.datetime.now())
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    user = orm.relation('User')

    categories = orm.relationship('Category', secondary=news_category, backref='news')

def get_categories(id_post):
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    categories_list=[]
    for i in db_sess.query(News).filter(News.id==id_post).first().categories:
        categories_list.append(i.name)
    return categories_list


