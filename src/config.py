import json
from pas_data import P

with open('src/config.json', 'r') as json_dump:
    data = json.load(json_dump)
DATA_BASE = data["DATA_BASE"]
HOST = data["HOST"]
PORT = data["PORT"]
DEBUG = data["DEBUG"]
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587
EMAIL = "qrtracker@yandex.ru"
PASSWORD = P
ADDRESS = f"{HOST}:{PORT}"  # поменять потом на домен
from functions import secret_key_generator

API_KEY = secret_key_generator(120)
