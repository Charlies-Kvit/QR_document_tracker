from flask import render_template
from string import ascii_letters
from phonenumbers import is_valid_number, parse
from itsdangerous import URLSafeTimedSerializer
from email.mime.text import MIMEText
from requests import get
import smtplib
import random
import re


def send_email(subject, recipients, link):
    from config import SMTP_SERVER, SMTP_PORT, EMAIL, PASSWORD
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    link = get("https://clck.ru/--", params={'url': link}).text
    html = render_template('mail_confirm_email.html', link=link, subject=subject)
    message = MIMEText(html, "html", "utf-8")
    message["Subject"] = subject
    message["From"] = EMAIL
    message["To"] = recipients
    server.sendmail(from_addr=EMAIL, to_addrs=recipients, msg=message.as_string())
    server.quit()


def secret_key_generator(length):
    key = list()
    for _ in range(int(length)):
        key.append(random.choice(ascii_letters))
    return ''.join(key)


def check_key(key):
    from config import API_KEY
    return key == API_KEY


def check_email(email):
    regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(regex_pattern, email))


def check_phone_number(phone_number):
    # phone_number = format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
    return is_valid_number(parse(phone_number, "RU"))


def get_int_phone_number(phone_number):
    answer = ""
    for el in phone_number:
        if el.isdigit():
            answer += el
    return answer


def generate_token(email):
    from app import app
    s = URLSafeTimedSerializer(app.secret_key)
    return s.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    from app import app
    s = URLSafeTimedSerializer(app.secret_key)
    try:
        email = s.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

