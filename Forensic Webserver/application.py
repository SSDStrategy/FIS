""" This is the main module for the Flask webserver """

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
    """
        The home page route function displays the login page, requests log in,
        and processes the login details provided
    """
    
    msg = request.method
    if msg == "GET":
        return render_template("index.html")
    elif msg == "POST":
        # Log login attempt
        name = request.form.get("name")
        password = request.form.get("password")
        login = {name : password}
        # Might need to make json_io a class and run the rest of
        # this routes code in the thread so that the main thread
        # can revert back to the normal webserver listening 
        
        auth_thread = Thread(target= json_io, args= (login,) )
        auth_thread.start()
        # Send JSON object to Authentication module
        return render_template("/options.html")
        
        
        # Process returned information
        # if(returned value)== True:
        # redirect to options page
        # else:
        # inform user

# Options page logic
@app.route("/options", methods = ["GET", "POST"])
def options():
    """
        The options page provides an initial means to the user
        to navigate to the required service.
    """
    
    # check authentication possibly by a session cookie
    # if authenticated then proceed
    msg = request.method
    if msg == "GET":
        return render.template("options.html")

    elif (msg == "POST") and # logout selected 


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

# Create page logic 
@app.route("/create", methods = ["GET", "POST"])
def create():
    """
        The create page allows a user to create a case
        by first entering its related metadata, after
        which the page is redirected to the edit page.
    """


# Delete page logic 
@app.route("/delete", methods = ["GET", "POST"])
def create():
    """
        The delete page allows a user to select and
        delete a case.
    """












        

app.run()
