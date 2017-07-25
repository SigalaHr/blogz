#!/usr/bin/env python

__author__ = "student"
__version__ = "1.0"
# July 2017
# Flask Blog App Continued re: LaunchCode lc-101
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/


import hashlib
import random
import string


def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


def make_password_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash_password = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash_password, salt)


def check_password_hash(password, hash_password):
    salt = hash_password.split(',')[1]
    return make_password_hash(password, salt) == hash_password
