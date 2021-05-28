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

""" Description: Define user model.
                 Specifies interaction with MongoDB Atlas
"""

# ============================================================================== #
#                                      IMPORTS       

from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

# ============================================================================== #
#                                      MODELS

class User:
    """ User Model """
    
    def start_session(self, user):
        """ Start new session """

        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        """ On signup: create new user object """

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address already in use" }), 400

        # Try to insert user into database
        if db.users.insert_one(user):
            return self.start_session(user)

        # If everything fails, return signup error
        return jsonify({ "error": "Signup failed" }), 400
    
    def signout(self):
        """ On signout: clear current session.
                        user must login again        
        """

        session.clear()
        return redirect('/')
    
    def login(self):
        """ On login: Find email in database and 
                      check whether password matches    
        """

        user = db.users.find_one({
            "email": request.form.get('email')
        })

        # If a user was found and if the password matches, start new session
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        # If everything fails, return invalid login
        return jsonify({ "error": "Invalid login credentials" }), 401