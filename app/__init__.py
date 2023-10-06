from flask import Flask

app = Flask(__name__)

USERS = []
CONTESTS = []

from app import views

from app import models
