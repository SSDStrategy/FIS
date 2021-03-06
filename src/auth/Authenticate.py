"""
    This module/microservice accepts a JSON object sent from the main
    webserver, which contains a username and encrypted password.
    It then verifies the values are present in the related database,
    after which sends a JSON object back to the webserver with the original
    username and appropriate authorisation level, or a failed login flag.
"""

import json

import bcrypt
import pyDes
import requests

from sys import path

path.append('..')
from core import my_salt
from data.UserRepository import UserRepository
from core.UserService import UserService

from flask import Flask, request

# Create a Flask webserver so that HTTP can be used to pass
# JSON objects between the applications 
app = Flask(__name__)

# Set encryption object 
encryptor = pyDes.triple_des("VeRy$ecret#1#3#5", pad=".")


# Create an HTTP URL/route that can be used by the main webserver
# to address HTTP traffic to
@app.route('/login', methods=['POST'])
def login():
    """
        Login is a single route-function containing all the necessary
        logic to authenticate a user.
    """

    login = request.json
    username = login[0]

    # Set the received encrypted password to a bytestring
    # of the received integer list to be able to decrypt
    encrypted_password = bytes(login[1])
    # Decrypt password and convert to UTF-8 string 
    password = encryptor.decrypt(encrypted_password)
    password = bcrypt.hashpw(password, my_salt)
    password = str(password)
    result = []

    # Fetch username and password from database**
    user_service = UserService(UserRepository())
    user = user_service.find_by_username(username=username)
    
    if user is None:
        result = [username, "FNN"]
    elif user.password == password:
        result = [user.username, user.auth_level]
    else:
        result = [user.username, "F"]

    # Return the result to the main webserver 
    result_json = json.dumps(result)
    http_header = {'Content-Type': 'application/json'}
    reply = requests.post('http://localhost:5000/update_users', headers=http_header, data=result_json)

    return 'Succeeded'


if __name__ == "__main__":
    # Run the instantiated Flask webserver
    app.run(host='127.0.0.1', port=5005)
