
""" This is the main module for the Flask webserver """

from flask import Flask, render_template, request, redirect, session
import json
import requests
import time
import pyDes

# Create Flask instance and set configurations
app = Flask(__name__)
app.secret_key = '1@#rTb47BK"_9'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200

# Instantiate encryption object
encryptor = pyDes.triple_des("VeRy$ecret#1#3#5", pad= ".")

# Initiate global dictionary to temporarily store authentication
# details until a user session is created
logged_in_users_flag = {}


@app.route("/", methods = ["GET", "POST"])
def login():
    """
        The home page route function displays the login page, requests log in,
        and processes the login details provided
    """
    global logged_in_users_flag
    msg = request.method
    if msg == "GET":
        return render_template("login.html")
    elif msg == "POST":
        # Log login attempt
        name = request.form.get("name")
        password = request.form.get("password")
        encrypted_password = (encryptor.encrypt(password))
        login = [name, list(encrypted_password)]
        login_json = json.dumps(login)
        http_header = {'Content-Type': 'application/json'}
        repy = requests.post('http://localhost:5005/', headers=http_header, data= login_json)
        time.sleep(4)
        if logged_in_users_flag[name] > 0:
            session['user_auth'] = logged_in_users_flag[name]
            del logged_in_users_flag[name]
            return redirect("/options")

            
@app.route("/update_users", methods = ["POST"])
def log_users():
    ''' Creates an entry to be stored temporarily in a global dictionary '''

    global logged_in_users_flag
    
    new_user = request.json
    logged_in_users_flag[new_user[0]] = new_user[1]
    print(logged_in_users_flag)
    return "successful"
              

# Options page logic
@app.route("/options", methods = ["GET", "POST"])
def options():
    """
        The options page provides an initial means to the user
        to navigate to the required service.
    """
    
    msg = request.method
    if msg == "GET":
        try:
            if session['user_auth'] > 0:
                print(session["user_auth"])
                return render_template("options.html")
        except:
                return 'you are not logged in'
    # check authentication possibly by a session cookie
    # if authenticated then proceed
    #msg = request.method
    #if msg == "GET":
        

        


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
