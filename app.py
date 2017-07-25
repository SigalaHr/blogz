#!/usr/bin/env python

__author__ = "student"
__version__ = "1.0"
# July 2017
# Flask Blog App Continued re: LaunchCode lc-101
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:abc123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'super_secret_key'
