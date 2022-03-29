import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import login_required 

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return "a"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        confirmacion = str(request.form.get('password_confirmation'))

        print(has_spaces(username))

        if password != confirmacion:
            return 'Passwords must be equal'

        username2 = username.strip()
        password2 = password.strip()
        confirmacion2 = confirmacion.strip()

        print(username2,password2,confirmacion2)
        return 'OK'
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        pass

    else:
        return render_template("login.html")

def has_spaces(string):
    for i in string:
        if i == ' ':
            return True
        
    return False