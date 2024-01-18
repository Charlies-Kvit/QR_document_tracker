import json
import os

with open('config.json', 'r') as json_dump:
    data = json.load(json_dump)
DATA_BASE = data["DATA_BASE"]
HOST = data["HOST"]
PORT = data["PORT"]
DEBUG = data["DEBUG"]
