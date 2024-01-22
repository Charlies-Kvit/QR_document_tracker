import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    middle_name = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    confirm = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    date_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    date_change = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    groups = orm.relationship('Group', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
