""" This is a the main module for the Flask webserver """

from flask import Flask, render_template, request, redirect
import json
from threading import Thread

# need to ensure correct configurations are set like for cookies
# and HTTPS 
app = Flask(__name__)

def json_io(login_dict):
    """
        Accepts an entered username and password related dictionary,
        converts it to a JSON object then sends it to the Auth module
        to confirm user exists.
    """

    print(login_dict)
    json.dumps(login_dict)

# Homepage logic 
@app.route("/", methods = ["GET", "POST"])
@app.route("/home", methods = ["GET", "POST"])
def homepage():
    msg = request.method
    if msg == "GET":
        return render_template("index.html")
    elif msg == "POST":
        # Log login attempt
        name = request.form.get("name")
        password = request.form.get("password")
        login = {name : password}
        auth_thread = Thread(target= json_io, args= (login,) )
        auth_thread.start()
        # Send JSON object to Authentication module
        return "successful"
        
        
        # Process returned information
        # if(returned value)== True:
        # redirect to options page
        # else:
        # inform user 
        

app.run()
