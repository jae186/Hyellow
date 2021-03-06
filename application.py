from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required

import requests
import urllib.parse
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#  Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hyellow.db")


# Index
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
        


# login
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # Ensure email was submitted
        if not request.form.get("email"):
            return render_template('error.html', error="must provide email")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('error.html', error="must provide password")

        # Query database for email
        emails_in_database = db.execute("SELECT * FROM users WHERE LOWER(email) == LOWER(:email)",
                          username=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(emails_in_database) != 1 or not check_password_hash(emails_in_database[0]["hash"], request.form.get("password")):
            return render_template('error.html', error="invalid email and/or password")

        # Remember which user has logged in
        session["user_id"] = emails_in_database[0]["id"]

        # Redirect user to home page
        return redirect("/swipe")


# signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        # Ensure a first name was submitted
        if not request.form.get("firstName"):
            return render_template('error.html', error="Must provide a first name")
        elif not request.form.get("lastName"):
            return render_template('error.html', error="Must provide a last name")
        elif not request.form.get("email"):
            return render_template('error.html', error="Must provide an email address")
        elif not request.form.get("password"):
            return render_template('error.html', error="Must provide a password")
        elif not request.form.get("confirmation"):
            return render_template('error.html', error="Must confirm your password")

        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
            
        if password != confirmation:
            return render_template('error.html', error="Password doesn't match")

        # Query the databse for the accounts with that email
        emails_in_database = db.execute("SELECT email FROM users WHERE email = :email",
                          email=email)

        if len(emails_in_database) != 0:
            return render_template('error.html', error="There is already an account with this email address")
        else:
            db.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (:firstName, :lastName, :email, :password)", firstName=firstName, lastName=lastName,
                        email=email, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
        
        # Query database for username
        account = db.execute("SELECT * FROM users WHERE email = :email",
                          email=email)

        # Remember which user has logged in
        session["user_id"] = account[0]["id"]
        
        # Redirect user to the swipe page
        return redirect('/aCoupleMoreThings')


# MBTI
MBTI = []
@app.route("/questionnaireMBTI/1", methods=["GET", "POST"])
def MBTI_1():
    MBTI_questions = [
        "After a tiring weekend you recharge by being with people instead of being by yourself",
        "Instead of thinking about present details, you'd rather think of future possibilities",
        "You analyze the problem to make decisions instead of just trusting your gut",
        "You'd rather plan your birthday compared to celebrating it spontaneously"]
    test = "MBTI"
    if request.method == "GET":
        return render_template("MBTI_1.html", questions = MBTI_questions, test = test)
    else:
        answer = request.form.get("answer")
        MBTI.append(answer)
        print(MBTI)
        return redirect(url_for('MBTI_2')) # change this index to somewhere else
    # add else statement if method == 'post' and return value of the personality type etc.


@app.route("/questionnaireMBTI/2", methods=["GET", "POST"])
def MBTI_2():
    if request.method == "GET":
        return render_template("MBTI_2.html")
    else:
        answer1 = request.form.get("answer")
        MBTI.append(answer1)
        print(MBTI)
        return redirect(url_for('MBTI_3')) # change this index to somewhere else
    # add else statement if method == 'post' and return value of the personality type etc.


@app.route("/questionnaireMBTI/3", methods=["GET", "POST"])
def MBTI_3():
    if request.method == "GET":
        return render_template("MBTI_3.html")
    else:
        answer = request.form.get("answer")
        MBTI.append(answer)
        print(MBTI)
        return redirect(url_for('MBTI_4')) # change this index to somewhere else
    # add else statement if method == 'post' and return value of the personality type etc.


@app.route("/questionnaireMBTI/4", methods=["GET", "POST"])
def MBTI_4():
    if request.method == "GET":
        return render_template("MBTI_4.html")
    else:
        answer = request.form.get("answer")
        MBTI.append(answer)
        print(MBTI)
        return redirect("/swipe") # change this index to somewhere else
    # add else statement if method == 'post' and return value of the personality type etc.


# acouplemorethings
@app.route("/aCoupleMoreThings", methods=["GET", "POST"])
def aCoupleMoreThings():
    if request.method == "GET":
        return render_template("acouplemorethings.html")
    else:
        # Ensure a first name was submitted
        education = request.form.get("education")
        school = request.form.get("school")
        major = request.form.get("major")
        job = request.form.get("job")
        height = request.form.get("height")
        bodyType = request.form.get("bodyType")
        ethnicity = request.form.get("ethnicity")
        religion = request.form.get("religion")
        politicalView = request.form.get("politicalView")

        # db.execute("INSERT INTO attributes (id, education, school, major, job, height, bodyType, ethnicity, religion, politicalView) VALUES (:id, :education, :school, :major, :job, :height, :bodyType, :ethnicity, :religion, :politicalView)", id=session["user_id"], education=education, school=school, major=major, job=job, height=height, bodyType=bodyType, ethnicity=ethnicity, religion=religion, politicalView=politicalView)
        db.execute("INSERT INTO attributes (id, education, school, job, height, bodyType, ethnicitiy, religion, politicalView) VALUES (:id, :education, :school, :job, :height, :bodyType, :ethnicity, :religion, :politicalView)", id=session["user_id"], education=education, school=school, job=job, height=height, bodyType=bodyType, ethnicity=ethnicity, religion=religion, politicalView=politicalView)
        return redirect("/questionnaireMBTI/1")


# seehowitworks
@app.route("/seehowitworks", methods=["GET", "POST"])
def seehowitworks():
    return render_template("seehowitworks.html")

# Swipe
@app.route("/swipe", methods=["GET", "POST"])
def swipe():
    if request.method == "GET":
        userInfo = db.execute("SELECT id AS userId, firstName FROM users ORDER BY RANDOM() LIMIT 1")
        userId = userInfo[0]['userId']
        firstName = userInfo[0]['firstName']
        print(userId)
        userAttributes = db.execute("SELECT age, city, country, MBTI, astroSign FROM attributes WHERE id=:userId", userId=userId)
        age = userAttributes[0]['age']
        city = userAttributes[0]['city']
        country = userAttributes[0]['country']
        MBTI = userAttributes[0]['MBTI']
        astroSign = userAttributes[0]['astroSign']
        attributesList = {'userId':userId, 'firstName':firstName, 'age':age, 'city':city, 'country':country, 'MBTI':MBTI, 'astroSign':astroSign}
        return render_template("swipe.html", attributesList=attributesList)
    # Code here



if __name__ == "__main__":
    app.run()
