from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import HOST, PORT, DEBUG
from waitress import serve
from data import db_session
from data.Users import User
from data.Groups import Group
from data.Group_users import GroupUsers
from data.Documents import Document


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template('base.html', title="Главная страница")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


if __name__ == '__main__':
    db_session.global_init("db/db.sqlalchemy")
    if DEBUG:
        app.run(HOST, port=PORT, debug=DEBUG)
    else:
        serve(app, host=HOST, port=PORT)
