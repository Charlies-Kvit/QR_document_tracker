import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Document(SqlAlchemyBase):
    __tablename__ = 'documents'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    tracker_file = sqlalchemy.Column(sqlalchemy.String, unique=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('groups.id'))
    group = orm.relationship('Group')
