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

""" Description: Define user-specific routes
"""

# ============================================================================== #
#                                      IMPORTS

from flask import Flask
from app import app
from user.models import User

# ============================================================================== #
#    

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()