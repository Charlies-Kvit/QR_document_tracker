import json
import os
from functions import secret_key_generator


class MailConfig(object):
    # ...
    """app.config["MAIL_SERVER"] = "app.debugmail.io"
    app.config["MAIL_PORT"] = 25
    app.config["MAIL_USERNAME"] = "7e68bb14-c07d-43af-9907-5348f2a4f565"
    app.config["MAIL_PASSWORD"] = "090a5a62-989a-4d64-a51b-cda2de507320"
    app.config["MAIL_USE_TLS"] = True"""
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']


with open('src/config.json', 'r') as json_dump:
    data = json.load(json_dump)
DATA_BASE = data["DATA_BASE"]
HOST = data["HOST"]
PORT = data["PORT"]
DEBUG = data["DEBUG"]
API_KEY = secret_key_generator(120)
