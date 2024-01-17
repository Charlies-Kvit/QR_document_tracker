import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class GroupUsers(SqlAlchemyBase):
    __tablename__ = 'group_users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    middle_name = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('groups.id'))
    group = orm.relationship('Group')
