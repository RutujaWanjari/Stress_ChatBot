# # -*- coding: utf-8 -*-
# __version__ = '0.1'
# from flask import Flask
# #from flask_debugtoolbar import DebugToolbarExtension
# app = Flask('project')
# app.config['SECRET_KEY'] = 'random'
# app.debug = True
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# #toolbar = DebugToolbarExtension(app)
# from project.controllers import *


# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
import os

#from flask_debugtoolbar import DebugToolbarExtension
app = Flask('project')
mongo = PyMongo(app)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'random'
app.debug = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#toolbar = DebugToolbarExtension(app)


# Use TLS true and SSL false, so that it wont give any authentication problem.
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'bot@instarem.com',
    MAIL_PASSWORD = 'InstaBot17',
))


# This will later contain address of customer support.
ADMINS = ['bot@instarem.com']

from flask_mail import Mail
mail = Mail(app)
from project.controllers import *
