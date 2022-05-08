import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

news_category = sqlalchemy.Table('news_category', SqlAlchemyBase.metadata,
                                 sqlalchemy.Column('news_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('news.id')),
                                 sqlalchemy.Column('category_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id')))


class Category(SqlAlchemyBase):
    __tablename__ = 'category'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # news = orm.relationship('News', secondary=news_category, backref='categories')

