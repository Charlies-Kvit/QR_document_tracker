from string import ascii_letters
from email_validate import validate
from phonenumbers import is_valid_number, parse
from flask_mail import Message
import random


def send_email(subject, sender, recipients, text_body, html_body):
    from app import mail
    mail.connect()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def secret_key_generator(length):
    key = list()
    for _ in range(int(length)):
        key.append(random.choice(ascii_letters))
    return ''.join(key)


def check_key(key):
    from config import API_KEY
    return key == API_KEY


def check_email(email):
    return validate(email)


def check_phone_number(phone_number):
    # phone_number = format_number(phone_number, PhoneNumberFormat.INTERNATIONAL)
    return is_valid_number(parse(phone_number, "RU"))


def get_int_phone_number(phone_number):
    answer = ""
    for el in phone_number:
        if el.isdigit():
            answer += el
    return answer
