import json
import os

from flask import Flask, session, render_template, request, jsonify, abort, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import login_required 

from werkzeug.security import check_password_hash, generate_password_hash

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
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        confirmacion = str(request.form.get('password_confirmation'))

        if password != confirmacion:
            return 'Passwords must be equal'

        username = username.strip()
        password  = password.strip()
        confirmacion = confirmacion.strip()

        if username == '' or password == '' or confirmacion == '':
            return 'Not valid credentials'

        # Validando que solo pueda existir un usuario

        res = db.execute("SELECT * FROM usuarios WHERE username = :username",
                        {"username": username}).fetchone()

        if res:
            return "User already taken"
        
        db.execute("INSERT INTO usuarios (username, hash) VALUES (:username, :hash)",
                  {"username": username, "hash": generate_password_hash(password)})
                  
        db.commit()


        return 'OK'
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == 'POST':
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))

        username = username.strip()
        password = password.strip()

        if username == "" or password == "":
            return redirect("/login")

        rows = db.execute("SELECT * FROM usuarios WHERE username = :nombre",
                        {"nombre": username}).fetchone()

        if len(rows) != 3 or not check_password_hash(rows[2],password):
            return redirect("/login")

        session["user_id"] = rows[0]

        return redirect('/')

    else:
        return render_template("login.html")

@app.route("/api/<isbn>")
def api(isbn):
    libro = db.execute("SELECT * FROM books WHERE isbn = :numero",
                        {"numero": isbn}).fetchone()
    if not libro:
        abort(404)
        
    return jsonify({"isbn": libro[0], "title": libro[1], "author": libro[2], "year": libro[3]})

@app.route("/logout",methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    return redirect("/")
    
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route("/<value>")
@login_required
def busqueda(value):
    value = value.lower()
    rows = db.execute("SELECT * FROM books WHERE lower(isbn) LIKE :value OR lower(title) LIKE :value OR lower(author) LIKE :value OR lower(year) LIKE :value", {
        "value": "%" + value + "%"}).fetchall()
    elementos = []
    for i in rows:
        elementos.append(list(i))
    return jsonify(elementos)



# https://www.namecheap.com/hosting/shared/
# https://dash.cloudflare.com/sign-up?pt=f
# Validacion intentos de password
# https://www.hostinger.es/