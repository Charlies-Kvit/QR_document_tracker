import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    group_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')
    documents = orm.relationship('Document', back_populates='group')
    group_users = orm.relationship('GroupUsers', back_populates='group')
