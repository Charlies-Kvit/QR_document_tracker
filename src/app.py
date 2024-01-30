from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import HOST, PORT, DEBUG, DATA_BASE, API_KEY, ADDRESS
from waitress import serve
from data import db_session
from data.Users import User
from data.Groups import Group
from data.Group_users import GroupUsers
from data.Documents import Document
from forms.user import RegisterForm, LoginForm
from functions import (secret_key_generator, check_email, check_phone_number, get_int_phone_number, send_email,
                       generate_token, confirm_token)

app = Flask(__name__)
app.secret_key = secret_key_generator(120)
app.config['SECURITY_PASSWORD_SALT'] = API_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    flash('test')
    context = {"title": "Главная страница", "current_user": current_user}
    return render_template('index.html', context=context)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    heading_h1 = "Регистрация"
    title = heading_h1
    if form.validate_on_submit():
        """if not form.agree.data:
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Вы не дали согласие на обработку персональных данных")"""
        if form.password.data != form.password_again.data:
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        logins = session.query(User).filter(User.login == str(form.login.data)).first()
        if logins:
            session.close()
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Логин занят, попробуйте другой")
        email = form.email.data
        emails = session.query(User).filter(User.email == str(email)).first()
        if emails:
            session.close()
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Почта уже занята, попробуйте другую")
        if not check_email(email):
            session.close()
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Такой почты не существует")
        phone = get_int_phone_number(form.phone_number.data)
        phones = session.query(User).filter(User.phone_number == int(phone)).first()
        if phones:
            session.close()
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Этот номер телефона уже занят, попробуйте другой.")
        if not check_phone_number(phone):
            session.close()
            return render_template("register.html", form=form, heading_h1=heading_h1, title=title,
                                   message="Такого номера телефона не существует")
        user = User(
            login=form.login.data,
            name=form.name.data,
            surname=form.surname.data,
            middle_name=form.middle_name.data,
            phone_number=int(phone),
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        session.close()
        return redirect(f"/need_confirm?email={form.email.data}")
    return render_template("register.html", form=form, heading_h1=heading_h1, title=title)


@app.route("/need_confirm")
def show_confirm():
    email = request.values.get("email")
    h1 = "Нужно подтверждение вашей почты"
    title = "Нужно подтверждение"
    session = db_session.create_session()
    check_email = session.query(User).filter(User.email == email).first()
    if not check_email:
        link = url_for("register")
        return render_template("need_confirm.html", h1=h1, title=title, msg="Такой почты в бд нет, "
                                                                            "зарегестрируйтесь", link=link)
    token = generate_token(email)
    # jwt.encode({'mail_confirm': user_id}, app.secret_key, algorithm='HS256')
    link = f"{ADDRESS}" + url_for("confirm_email", token=token)
    send_email("Подтверждение почты", email, link)
    return render_template("need_confirm.html", h1=h1, title=title)


@app.route("/confirm_email")
def confirm_email():
    token = request.values.get("token")
    try:
        email = confirm_token(token)
        assert not email is False
    except:
        h1 = "Нужно подтверждение вашей почты"
        title = "Нужно подтверждение"
        return render_template("need_confirm.html", h1=h1, title=title, msg="Токен просрочен, на почту"
                                                                            " повторно отправлено письмо")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    user.confirm = True
    db_sess.commit()
    db_sess.close()
    return redirect("/login?confirmed=true")


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    heading_h1 = "Авторизация"
    title = heading_h1
    if request.values.get("confirmed"):
        msg = "Почта успешно была подтверждена!"
    else:
        msg = ""
    if form.validate_on_submit():
        session = db_session.create_session()
        user_name = form.login_email.data
        if "@" in user_name:
            user = session.query(User).filter(User.email == user_name).first()
        else:
            user = session.query(User).filter(User.login == user_name).first()
        if not user:
            session.close()
            return render_template("login.html", heading_h1=heading_h1, title=title, form=form,
                                   message="Такой пользователь не найден")
        if not user.check_password(form.password.data):
            session.close()
            return render_template("login.html", heading_h1=heading_h1, title=title, form=form,
                                   message="Неверный пароль")
        if not user.confirm:
            user_id = user.id
            email = user.email
            session.close()
            return render_template("login.html", heading_h1=heading_h1, title=title, form=form,
                                   message=f"Почта не подтверждена. "
                                           f"<a href='/need_confirm?user_id={user_id}&email={email}'>Отправить повторно?</a>")
        login_user(user, remember=form.remember_me.data)
        session.close()
        return redirect("/")
    return render_template("login.html", heading_h1=heading_h1, title=title, form=form, message=msg)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

"""
@app.route("/lms")
@login_required
def lms():
    """


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


if __name__ == '__main__':
    db_session.global_init(DATA_BASE)
    if DEBUG:
        app.run(HOST, port=PORT, debug=DEBUG)
    else:
        serve(app, host=HOST, port=PORT)
