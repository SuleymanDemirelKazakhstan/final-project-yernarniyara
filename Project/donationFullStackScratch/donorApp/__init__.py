from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:8432/donor_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'superdupersecretkey123'

db = SQLAlchemy(app)
manager = LoginManager(app)

from donorApp import models, routes
