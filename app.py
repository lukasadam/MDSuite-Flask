# ============================================================================== #

# Copyright 2021 by Lukas Adam, gm.lukas.adam@gmail.com
# All rights reserved.
# This file is part of the MD Software Suite
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

__author__      = "Lukas Adam"
__copyright__   = "Copyright 2021, MDSuite"
__contact__ = "gm.lukas.adam@gmail.com"
__date__ = "2021/05/28"
__version__ = "0.0.1"

""" Description: Sets up flask application, defines top-level routes
                 and connects to MongoDB Atlas
"""

# ============================================================================== #
#                                      IMPORTS

import os 
import sys
from functools import wraps

from flask import Flask, render_template, session, redirect
from pymongo import MongoClient

# ============================================================================== #
#                                   CONFIGURATIONS

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Database
client = MongoClient(app.secret_connection_string)
db = client.user_login_system

# ============================================================================== #
#                                     DECORATORS

# Login decorator
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# ============================================================================== #
#                                     ROUTES

# User-specific routes
from user import routes

# Shared routes
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')