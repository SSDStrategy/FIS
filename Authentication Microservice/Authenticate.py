"""
    This module accepts a JSON object and verifies
    its values are present in the related database
"""

from threading import Thread
from flask import Flask, request
import requests
import json 

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def login():
    login = request.json 
    print(login)
    print(type(login))
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
