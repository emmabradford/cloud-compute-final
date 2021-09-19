from flask import Flask, g, render_template, flash, request, url_for, redirect, session
#from dbconnect import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import csv
import sqlite3
import logging

app = Flask(__name__)

#conn = sqlite3.connect('project1.db')
#cur = conn.cursor()
#cur.execute("""DROP TABLE IF EXISTS users""")
#cur.execute("""CREATE TABLE users
#           (username text, password text, email text, givenName text, familyN    ame text)""")

#with open('users.csv', 'r') as f:
#    reader = csv.reader(f.readlines()[1:])  # exclude header line
#    cur.executemany("""INSERT INTO users VALUES (?,?,?,?,?)""",
#                    (row for row in reader))

#conn.commit()
#conn.close()

#logging.basicConfig()

DATABASE = "/var/www/FlaskApp/FlaskApp/project1.db"

app.config.from_object(__name__)
#logging.basicConfig(filename='api.log',level=logging.DEBUG)
#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/', methods=["GET","POST"])
def homepage():
    error = ''
    try:        
        if request.method == "POST":
	
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            #username = execute_query("""SELECT * FROM users WHERE username = ?""", [username.title()])
            #return redirect(url_for('<attempted_username>'))
            user = execute_query("""SELECT * FROM users WHERE username = ?""", [attempted_username])
            psw = execute_query("""SELECT password FROM users WHERE username = ?""", [attempted_username])
            #return redirect(url_for('info'))
            # if attempted_username == "admin" and attempted_password == "password":
            #if attempted_password == "test" and attempted_userName == "joe":
            if attempted_password == psw[0][0].replace(" ", ""):
                #return redirect(url_for('<username>'))
                return redirect(url_for('info'))
                #return render_template("info.html")
                error = ""
            else:
                error = "Invalid credentials. Try Again."


        return render_template("main1.html")
    except Exception as e:
        return render_template("main1.html")

class SignUp(Form):
    familyName = TextField('Family Name')
    givenName = TextField('Given Name')
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service', [validators.Required()])
    

@app.route('/signUp', methods=["GET","POST"])
def signUp():
    try:
        form = SignUp(request.form)
        if request.method == "POST" and form.validate():
            familyName = form.familyName.data
            givenName = form.givenName.data
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('signUp.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking, givenName, familyName) VALUES (%s, %s, %s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart(givenName), thwart(familyName)))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('info'))
        return render_template("signUp.html", form=form)
    except Exception as e:
        return(str(e))

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""")
    return '<br>'.join(str(row) for row in rows)

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/<username>')
def sortby(username):
    rows = execute_query("""SELECT * FROM users WHERE username = ?""", [username])
    #return "userne"    
    return '<br>'.join(str(row) for row in rows)
#    return render_template("info.html")

if __name__ == "__main__":
    app.run(debug=True)
