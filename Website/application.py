""" This is the main module for the Flask webserver """

from flask import Flask, render_template, request, redirect
from flask_session import Session 
#from flask_talisman import Talisman -> required if using HTTPs to set flask config
import json
from time import sleep # For testing purposes
import requests
import time

# need to ensure correct configurations are set like for cookies
# and HTTPS 
app = Flask(__name__)
#Talisman(app)

logged_in_users = {}

# Login page logic 
@app.route("/", methods = ["GET", "POST"])
def login():
    """
        The home page route function displays the login page, requests log in,
        and processes the login details provided
    """
    global logged_in_users
    msg = request.method
    if msg == "GET":
        return render_template("login.html")
    elif msg == "POST":
        # Log login attempt
        name = request.form.get("name")
        password = request.form.get("password")
        login = [name, password]
        login_json = json.dumps(login)
        http_header = {'Content-Type': 'application/json'}
        repy = requests.post('http://localhost:5005/', headers=http_header, data= login_json)
        time.sleep(2)
        if logged_in_users[name] == True:
            return redirect("/options")
            
        #print(login_result)
            
        #if login_result == True:
        #return render_template("options.html")
        #else:
        #return "Login Failed"
        #time.sleep(3)
        #   set session value 
        # inform user
        #if (request.headers.get('Content-Type') == 'application/json'):
            
@app.route("/update_users", methods = ["POST"])
def log_users():
    global logged_in_users
    
    new_user = request.json
    logged_in_users[new_user[0]] = new_user[1]
    print(logged_in_users)
    return "successful"
              

# Options page logic
@app.route("/options", methods = ["GET", "POST"])
def options():
    """
        The options page provides an initial means to the user
        to navigate to the required service.
    """
    
    # check authentication possibly by a session cookie
    # if authenticated then proceed
    #msg = request.method
    #if msg == "GET":
    return render_template("options.html")

    #elif (msg == "POST") and # logout selected 


# Create page logic 
@app.route("/create", methods = ["GET", "POST"])
def create():
    """
        The create page allows a user to create a case
        by first entering its related metadata, after
        which the page is redirected to the edit page.
    """


# Search page logic
@app.route("/search", methods = ["GET", "POST"])
def search():
    """
        The search page allows a user to enter a case number,
        creation date, or/and name substring to reveal the cases 
        whose values contain the entered ones.       
    """

# Edit page logic
@app.route("/edit", methods = ["GET", "POST"])
def edit():
    """
        The edit case page requires a user to enter a case
        number for a case to edit then redirects to the
        specific case.
    """


# Delete page logic 
@app.route("/delete", methods = ["GET", "POST"])
def delete():
    """
        The delete page allows a user to select and
        delete a case.
    """


        

app.run()
