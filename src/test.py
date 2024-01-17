from data import db_session
from data.Users import User
from data.Groups import Group

db_session.global_init("db/db.sqlalchemy")
db_sess = db_session.create_session()
users = db_sess.query(User).all()
db_sess.close()
for el in users:
    print(el)
