"""
    This module/microservice accepts a JSON object sent from the main
    webserver, which contains a username and encrypted password.
    It then verifies the values are present in the related database,
    after which sends a JSON object back to the webserver with the original
    username and appropriate authorisation level, or a failed login flag.
"""

from flask import Flask, request, make_response
import requests
import json
import hashlib
import pyDes

# Create a Flask webserver so that HTTP can be used to pass
# JSON objects between the applications 
app = Flask(__name__)

# Set encryption object 
encryptor = pyDes.triple_des("VeRy$ecret#1#3#5", pad= ".")

# Create an HTTP URL/route that can be used by the main webserver
# to address HTTP traffic to
@app.route('/login', methods = ['POST'])
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
    password = password.decode()
    
    # **Try fetch username and password from database**
    # **result = [name, authorisation_level]**
    result = []
    if username == 'Michael' and password == "1234":
        result = [username, 1]
    elif username == 'Amy' and password == "5678":
        result = [username, 2]
    elif username == 'Aaaa' and password == "abc":
        result = [username, "FNN"]
    elif username == 'Wes' and password == "aefg":
        result = [username, "F3"]
        
        
    # Return the result to the main webserver 
    result_json = json.dumps(result)
    http_header = {'Content-Type': 'application/json'}
    repy = requests.post('http://localhost:5000/update_users', headers=http_header, data= result_json)

    return 'Succeeded'



# Run the instantiated Flask webserver
app.run(port = 5005)
