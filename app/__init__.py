
from flask import Flask
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

USERS = []  # a list of User-type objects
CONTESTS = []   # a list of Contest-type objects
ENDPOINT = 'http://127.0.0.1:5000'

from app import forms
from app import tests
from app import views
from app import models
from app import views_all
