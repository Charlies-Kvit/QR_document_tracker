from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import HOST, PORT, DEBUG
from waitress import serve
from data import db_session
from data.Users import User
from data.Groups import Group
from data.Group_users import GroupUsers
from data.Documents import Document
from forms.user import RegisterForm, LoginForm
from functions import secret_key_generator


app = Flask(__name__)
app.secret_key = secret_key_generator(120)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    context = {"title": "Главная страница", "current_user": current_user}
    return render_template('index.html', context=context)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit()
    return render_template("register.html", form=form, heading_h1="Регистрация", title="Регистрация")


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
