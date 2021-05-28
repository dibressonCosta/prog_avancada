from config import Config
from flask import Flask
import flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

mongodb_client = PyMongo(app, uri="mongodb+srv://root:root@progavan.qrww5.mongodb.net/ProgAvan?retryWrites=true&w=majority")
db = mongodb_client.db

from app import routes
