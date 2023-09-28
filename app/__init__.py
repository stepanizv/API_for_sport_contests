from flask import Flask

app = Flask(__name__)

USERS = []  # list for type User objects

from app import views

from app import models
