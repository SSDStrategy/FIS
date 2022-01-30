""" This is the main module for the Flask webserver """

from flask import Flask, render_template, request, redirect, session, Response, url_for
import json
import requests
import time
import pyDes
from threading import Thread
import logging

from core.Authorization import Authorizer
from core.CaseService import CaseService
from data import Case, User
from data.CaseRepository import CaseRepository

# Create Flask instance and set configurations
from web.authorization import get_user

app = Flask(__name__)
app.secret_key = '1@#rTb47BK"_9'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # Set session cookie to 30mins

# Set up separate filehandler and formatter for Flask logger: app.logger
# so that ceratin logs can be logged to a log file
format2 = '%(levelname)s:%(asctime)s%(message)s'
handler2 = logging.FileHandler('log.log', mode= 'a')
handler2.setLevel(logging.WARNING)
formatter2 = logging.Formatter(format2)
handler2.setFormatter(formatter2)
app.logger.addHandler(handler2)
case_service = CaseService(CaseRepository(), Authorizer())

# Instantiate encryption object
encryptor = pyDes.triple_des("VeRy$ecret#1#3#5", pad=".")

# Initiate global dictionary to temporarily store authentication
# details until a user session is created.
logged_in_users_flag = {}


def check_logged_in(html_file, msg):
    """ Checks authorisation """
    try:
        if (session['user_auth'][1] == 1 or
                session['user_auth'][1] == 2 or
                session['user_auth'][1] == 3):
            return render_template(html_file, message=msg)
    except KeyError:
        return redirect(url_for('login', message="You are not logged in"))

    

# Initial login URL logic follows
@app.route("/", methods=["GET", "POST"])
def login():
    """
        The home page route function displays a login page containing
        a username and password input, then processes the submitted login
        details and creates a unique user session with a related authorisation
        level.
    """

    global logged_in_users_flag
    msg = request.method

    if msg == "GET":
        if request.args.get('message'):
            return render_template("login.html", message=request.args.get('message'))
        else:
            return render_template("login.html")

    elif msg == "POST":
        try:
            name = request.form.get("name")
            password = request.form.get("password")
            encrypted_password = (encryptor.encrypt(password))
            # The encytped password is converted to a list of integers to make it
            # JON serialisable as it is returned as a bytestring.
            # The list is put into another list also containing the username entered.
            login = [name, list(encrypted_password)]
            login_json = json.dumps(login)

            # Send to the Authentication microservice.
            http_header = {'Content-Type': 'application/json'}
            reply = requests.post('http://localhost:5005/login', headers=http_header, data=login_json)
            # Sleep the code so that any communication delay won't create
            # a fault as the microservice responds to the "log_users" URL below.
            time.sleep(4)
        except:
            return render_template("login.html", message="Login failed. Please try again")

        # Check the values returned from the Authentication microservice
        try:
            # Check the flag received from the microservice and temporarily
            # stored in the logged_in_users_flag dictionary 
            if ((logged_in_users_flag[name] == 1) or
                    (logged_in_users_flag[name] == 2) or
                    (logged_in_users_flag[name] == 3)):

                # Create a session and assign the user's name and auth level to it 
                session['user_auth'] = [name, logged_in_users_flag[name]]
                del logged_in_users_flag[name]
                # Log login in a separate thread
                log_message = session['user_auth'][0] + ' logged in at auth level of: ' + \
                              str(session['user_auth'][1])
                log_thread = Thread(target= app.logger.warning, args=(log_message,))
                log_thread.start()
                # **Log login outcome**
                return redirect("/cases")
            #TODO add an F
            elif logged_in_users_flag[name] == "F":
                # **Log login outcome**
                return render_template("login.html", message="Login Failed. Please try again")
            elif logged_in_users_flag[name] == "FNN":
                # **Log login outcome**
                return render_template("login.html", message="Username does not exist. Please try again")
            elif logged_in_users_flag[name] == "F1":
                # **Log login outcome**
                return render_template("login.html", message="Incorrect password. Please try again. two more attempts")
            elif logged_in_users_flag[name] == "F2":
                # **Log login outcome**
                return render_template("login.html", message="Incorrect password. Please try again. one more attempts")
            elif logged_in_users_flag[name] == "F3":
                # **Log login outcome**
                return render_template("login.html",
                                       message="Incorrect password. Your account has been locked please contact admin")

        except:
            return render_template("login.html", message="Login failed. Please try again.")


@app.route("/update_users", methods=["POST"])
def log_users():
    ''' Creates an entry to be stored temporarily in a global dictionary. '''

    global logged_in_users_flag

    new_user = request.json
    logged_in_users_flag[new_user[0]] = new_user[1]
    return "successful"


# Options URL logic
@app.route("/options", methods=["GET", "POST"])
def options():
    """
        The options page provides an initial means to the user
        to navigate to the required service.
    """

    msg = request.method
    if msg == "GET":
        result = check_logged_in("options.html", "Please select below what you would like to do:")
        return result

    # Create URL logic


@app.route("/create", methods=["GET", "POST"])
def create():
    """
        The create page allows a user to create a case
        by first entering its related metadata.
    """

    if request.method == 'GET':
        return render_template("create.html")
    elif request.method == 'POST':
        logged_user: User = get_user(request)
        case = Case(logged_user.user_id, name=request.form['name'], description=request.form['description'])
        case_service.save(case)

        return render_template("cases.html")


# Search URL logic
@app.route("/cases", methods=["GET", "POST"])
def search():
    """
        The search page allows a user to enter a case number,
        creation date, or/and name substring to reveal the cases 
        whose values contain the entered ones.       
    """
    page_size = request.args.get('page_size', 1000, int)
    page_number = request.args.get('page_number', 1, int)
    cases = case_service.find_all(page_size=page_size, page_number=page_number)
    return render_template("cases.html", cases=cases)


# Edit URL logic
@app.route("/edit", methods=["GET", "POST"])
def edit():
    """
        The edit case page requires a user to enter a case
        number for a case to edit then redirects to the
        specific case.
    """
    if request.method == 'GET':
        case_id = request.args.get('case_id')
        case = case_service.find_by_id(case_id)

        return render_template("edit.html", case=case)

    elif request.method == 'POST':
        case_id = request.form['case_id']
        case = case_service.find_by_id(case_id)
        case.name = request.form['name']
        case.description = request.form['description']

        return render_template("cases.html")


# Logout URL logic
@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
        To log out.
    """
    # **Log logout**

    try:
        name = session["user_auth"][0]
        name_json = json.dumps(name)
        # Send to the Authentication microservice to process and update database.
        http_header = {'Content-Type': 'application/json'}
        reply = requests.post('http://localhost:5005/logout', headers=http_header, data=name_json)
        username = session['user_auth'][0]
        session.pop('user_auth', None)
        log_message = username + ' logged out'
        log_thread = Thread(target= app.logger.warning, args=(log_message,))
        log_thread.start()
        return "logout successful"
    except:
        return "logout unsuccessful"


if __name__ == '__main__':
    # Run the Flask webserver
    app.run(port=5000)
