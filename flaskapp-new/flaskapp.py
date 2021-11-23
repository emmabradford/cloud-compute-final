from flask import Flask, session, g, render_template, flash, request, url_for, redirect, session
#from dbconnect import connection
#from wtforms import Form, BooleanField, TextField, PasswordField, validators
#from passlib.hash import sha256_crypt
#from flask_login import login_required, current_user
from MySQLdb import escape_string as thwart
import gc
import csv
import sqlite3
import logging
#import pandas as pd
#import numpy as np


app = Flask(__name__)
app.secret_key = 'secreeeet'

conn = sqlite3.connect('/var/www/html/flaskapp/better.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS households""")
cur.execute("""CREATE TABLE households
           (Hshd_num text, Loyalty_flag text, Age_range text, Marital_status text, Income_range text, Homeowner_desc text, Hshd_composition text, Hshd_size text, Children text)""")

with open('/var/www/html/flaskapp/400_households.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO households VALUES (?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))

cur.execute("""DROP TABLE IF EXISTS transactions""")
cur.execute("""CREATE TABLE transactions
           (Hshd_num text, Basket_num text, Date text, Product_num text, Spend text, Units text, Store_region text, Week_num text, Year text)""")

with open('/var/www/html/flaskapp/400_transactions.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))

cur.execute("""DROP TABLE IF EXISTS products""")
cur.execute("""CREATE TABLE products
           (Product_num text, Department text, Commodity text, Brand_type text, Natural_organic_flag text)""")

with open('/var/www/html/flaskapp/400_products.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO products VALUES (?,?,?,?,?)""",
                    (row for row in reader))


conn.commit()
conn.close()

DATABASE = "/var/www/html/flaskapp/better.db"
#USERNAME = ""
FILES = ['data/400_households.csv','data/400_products.csv','data/400_transactions.csv']
app.config.from_object(__name__)

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
	
            #attempted_username = request.form['username']
            #attempted_password = request.form['password']
            #user = execute_query("""SELECT * FROM users WHERE username = ?""", [attempted_username])
            #psw = execute_query("""SELECT password FROM users WHERE username = ?""", [attempted_username])
            #if attempted_password == psw[0][0].replace(" ", ""):
                #return redirect(url_for('<username>'))
                #USERNAME = attempted_username
            #    session['username'] = attempted_username

            return redirect(url_for('info'))
#            else:
#                error = "Invalid credentials. Try Again."


        return render_template("main1.html")
    except Exception as e:
        return render_template("main1.html")

#class SignUp(Form):
#    familyName = TextField('Family Name')
#    givenName = TextField('Given Name')
#    username = TextField('Username', [validators.Length(min=1, max=20)])
#    email = TextField('Email Address', [validators.Length(min=1, max=50)])
#    password = PasswordField('New Password', [
#        validators.Required(),
#        validators.EqualTo('confirm', message='Passwords must match')
#    ])
#    confirm = PasswordField('Repeat Password')
#    accept_tos = BooleanField('I accept the Terms of Service', [validators.Required()])
    
'''
@app.route('/signUp', methods=["GET","POST"])
def signUp():
    try:
        form = SignUp(request.form)
        if request.method == "POST" and form.validate():
            familyName = form.familyName.data
            givenName = form.givenName.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            session['username'] = username
            x = execute_query("""SELECT * FROM users WHERE username = ?""",     [username])

            if len(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('signUp.html', form=form)

            else:
                c = execute_query("""INSERT INTO users (username, password, email, givenName, familyName) VALUES (?, ?, ?, ?, ?)""",
                          (username, password, email, givenName, familyName))
                #USERNAME = username
                get_db().commit()
                #curr.commit()
                flash("Thanks for registering!")
                #c.close()
                #conn.close()
                #gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('info'))
        return render_template("signUp.html", form=form)
    except Exception as e:
        return(str(e))
'''

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""")
    return '<br>'.join(str(row) for row in rows)

@app.route('/info')
#@login_required
def info():
    #name, email, givien, family
    #uname = current_user.name
    #uname = session['username']
    #data = execute_query("""SELECT * FROM users WHERE username = ?""", [uname])
    #data =  execute_query("""SELECT * FROM users WHERE username = ?""", [uname])

    #email = data[0][2].replace(" ", "")
    #given = data[0][3].replace(" ", "")
    #family =data[0][4].replace(" ", "")
    query1 = execute_query("""SELECT * FROM households ORDER BY Hshd_num LIMIT 20""")
    query2 = execute_query("""SELECT * FROM transactions ORDER BY Basket_num LIMIT 20""")
    query3 = execute_query("""SELECT * FROM transactions ORDER BY Date LIMIT 20""")
    query4 = execute_query("""SELECT * FROM transactions ORDER BY Product_num LIMIT 20""")
    query5 = execute_query("""SELECT * FROM products ORDER BY Department LIMIT 20""")
    query6 = execute_query("""SELECT * FROM products ORDER BY Commodity LIMIT 20""")





    return render_template("info.html", query1=query1, query2=query2, query3=query3, query4=query4, query5=query5, query6=query6)

#@app.route('/user')
#def find():
#    rows = execute_query("""SELECT * FROM users WHERE username = ?""", [USERNAME])
#    return '<br>'.join(str(row) for row in rows)

@app.route('/query1')
def query1():
	query1 = execute_query("""SELECT * FROM households ORDER BY Hshd_num LIMIT 20""")
	return render_template("query1.html", query1=query1)

@app.route('/query2')
def query2():
	query2 = execute_query("""SELECT * FROM transactions ORDER BY Basket_num LIMIT 20""")
	return render_template("query2.html", query2=query2)

@app.route('/query3')
def query3():
	query3 = execute_query("""SELECT * FROM transactions ORDER BY Date LIMIT 20""")
	return render_template("query3.html", query3=query3)

@app.route('/query4')
def query4():
	query4 = execute_query("""SELECT * FROM transactions ORDER BY Product_num LIMIT 20""")
	return render_template("query4.html", query4=query4)

@app.route('/query5')
def query5():
	query5 = execute_query("""SELECT * FROM products ORDER BY Department LIMIT 20""")
	return render_template("query5.html", query5=query5)

@app.route('/query6')
def query6():
	query6 = execute_query("""SELECT * FROM products ORDER BY Commodity LIMIT 20""")
	return render_template("query6.html", query6=query6)


@app.route('/<username>')
def sortby(username):
    rows = execute_query("""SELECT * FROM users WHERE username = ?""", [username])
    #return "userne"    
    return '<br>'.join(str(row) for row in rows)
#    return render_template("info.html")

if __name__ == "__main__":
    app.run(debug=True)
