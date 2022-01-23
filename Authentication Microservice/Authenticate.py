"""
    This module accepts a JSON object and verifies
    its values are present in the related database
"""

from threading import Thread
from flask import Flask, request
import requests
import json
import hashlib
import pyDes

app = Flask(__name__)
encryptor = pyDes.triple_des("VeRy$ecret#1#3#5", pad= ".")

@app.route('/', methods = ['POST'])
def login():
    login = request.json
    name = login[0]
    encrypted_password = bytes(login[1])
    password = encryptor.decrypt(encrypted_password)
    password = password.decode()
    print(password)
    # check database for username and password 
    #result = [validity, authorisation_level]
    result = [login[0], True]
    result_json = json.dumps(result)
    http_header = {'Content-Type': 'application/json'}
    repy = requests.post('http://localhost:5000/update_users', headers=http_header, data= result_json)

    return 'Succeeded'

#x = threading.Thread(target = x)
#x.start()

app.run(port = 5005)
