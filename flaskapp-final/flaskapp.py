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
import os
from os.path import join, dirname, realpath


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

'''
@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""")
    return '<br>'.join(str(row) for row in rows)
'''

@app.route('/info')
#@login_required
def info():
    #upload = request.files['file']
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

@app.route('/query1')
def query1():
	query1 = execute_query("""SELECT h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, p.Department, p.Commodity FROM (( HOUSEHOLDS AS h LEFT JOIN TRANSACTIONS AS t ON h.Hshd_num = t.Hshd_num) LEFT JOIN PRODUCTS AS p ON t.Product_num = p.Product_num) ORDER BY h.Hshd_num;""")
	return render_template("query1.html", query1=query1)

@app.route('/query2')
def query2():
	query2 = execute_query("""SELECT t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, p.Department, p.Commodity FROM transactions AS t LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num LEFT JOIN products AS p ON t.Product_num = p.Product_num ORDER BY t.Basket_num LIMIT 20;""")
	return render_template("query2.html", query2=query2)

@app.route('/query3')
def query3():
	query3 = execute_query("""SELECT t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, p.Department, p.Commodity FROM transactions AS t LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num LEFT JOIN products AS p ON t.Product_num = p.Product_num ORDER BY t.Date LIMIT 20;""")
	return render_template("query3.html", query3=query3)

@app.route('/query4')
def query4():
	query4 = execute_query("""SELECT t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, p.Department, p.Commodity FROM transactions AS t LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num LEFT JOIN products AS p ON t.Product_num = p.Product_num ORDER BY t.Product_num LIMIT 20;""")
	return render_template("query4.html", query4=query4)

@app.route('/query5')
def query5():
	query5 = execute_query("""SELECT p.Department, p.Commodity, t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children FROM products AS p LEFT JOIN transactions AS t ON p.Product_num = t.Product_num LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num ORDER BY p.Department LIMIT 20;""")
	return render_template("query5.html", query5=query5)

@app.route('/query6')
def query6():
	query6 = execute_query("""SELECT p.Department, p.Commodity, t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children FROM products AS p LEFT JOIN transactions AS t ON p.Product_num = t.Product_num LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num ORDER BY p.Commodity LIMIT 20;""")
	return render_template("query6.html", query6=query6)

'''
@app.route('/<username>')
def sortby(username):
    rows = execute_query("""SELECT * FROM users WHERE username = ?""", [username])
    #return "userne"    
    return '<br>'.join(str(row) for row in rows)
#    return render_template("info.html")
'''
if __name__ == "__main__":
    app.run(debug=True)


@app.route('/upload')
def uploadPage():
	return render_template('upload.html')

UPLOAD_FOLDER = '/var/www/html/flaskapp/newcsvs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET','POST'])
def upload():
	file = request.files['file']
	if file.filename != '':
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(file_path)
	return redirect(url_for('upload'))


conn2 = sqlite3.connect('/var/www/html/flaskapp/better2.db')
cur2 = conn2.cursor()
cur2.execute("""DROP TABLE IF EXISTS households""")
cur2.execute("""CREATE TABLE households(Hshd_num text, Loyalty_flag text, Age_range text, Marital_status text, Income_range text, Homeowner_desc text, Hshd_composition text, Hshd_size text, Children text)""")

with open('/var/www/html/flaskapp/newcsvs/400_households.csv', 'r') as f:
	reader = csv.reader(f.readlines()[1:])  # exclude header line
	cur2.executemany("""INSERT INTO households VALUES (?,?,?,?,?,?,?,?,?)""",(row for row in reader))
cur2.execute("""DROP TABLE IF EXISTS transactions""")
cur2.execute("""CREATE TABLE transactions(Hshd_num text, Basket_num text, Date text, Product_num text, Spend text, Units text, Store_region text, Week_num text, Year text)""")
	
with open('/var/www/html/flaskapp/newcsvs/400_transactions.csv', 'r') as f:
	reader = csv.reader(f.readlines()[1:])  # exclude header line
	cur2.executemany("""INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)""",(row for row in reader))
cur2.execute("""DROP TABLE IF EXISTS products""")
cur2.execute("""CREATE TABLE products(Product_num text, Department text, Commodity text, Brand_type text, Natural_organic_flag text)""")
with open('/var/www/html/flaskapp/400_products.csv', 'r') as f:
	reader = csv.reader(f.readlines()[1:])  # exclude header line
	cur2.executemany("""INSERT INTO products VALUES (?,?,?,?,?)""",(row for row in reader))
	
conn2.commit()
conn2.close()

DATABASE2 = "/var/www/html/flaskapp/newcsvs/better2.db"
#USERNAME = ""
#FILES = ['data/400_households.csv','data/400_products.csv','data/400_transactions.csv']
#app.config.from_object(__name__)

def connect_to_database_again():
    return sqlite3.connect(app.config['DATABASE'])

def get_db2():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database_again()
    return db

@app.teardown_appcontext
def close_connection2(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query2(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows
@app.route('/query12')
def query12():
	query1 = execute_query("""SELECT h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, p.Department, p.Commodity FROM (( HOUSEHOLDS AS h LEFT JOIN TRANSACTIONS AS t ON h.Hshd_num = t.Hshd_num) LEFT JOIN PRODUCTS AS p ON t.Product_num = p.Product_num) ORDER BY h.Hshd_num;""")
	return render_template("query1.html", query1=query1)
@app.route('/query22')
def query22():
	query2 = execute_query("""SELECT t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, p.Department, p.Commodity FROM transactions AS t LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num LEFT JOIN products AS p ON t.Product_num = p.Product_num ORDER BY t.Basket_num LIMIT 20;""")
	return render_template("query2.html", query2=query2)
@app.route('/query32')
def query32():
	query3 = execute_query("""SELECT t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, p.Department, p.Commodity FROM transactions AS t LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num LEFT JOIN products AS p ON t.Product_num = p.Product_num ORDER BY t.Date LIMIT 20;""")
	return render_template("query3.html", query3=query3)
@app.route('/query42')
def query42():
	query4 = execute_query("""SELECT t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children, p.Department, p.Commodity FROM transactions AS t LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num LEFT JOIN products AS p ON t.Product_num = p.Product_num ORDER BY t.Product_num LIMIT 20;""")
	return render_template("query4.html", query4=query4)	
@app.route('/query52')
def query52():
	query5 = execute_query("""SELECT p.Department, p.Commodity, t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children FROM products AS p LEFT JOIN transactions AS t ON p.Product_num = t.Product_num LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num ORDER BY p.Department LIMIT 20;""")
	return render_template("query5.html", query5=query5)
@app.route('/query62')
def query62():
	query6 = execute_query("""SELECT p.Department, p.Commodity, t.Basket_num, t.Date, t.Product_num, t.Spend, t.Units, t.Store_region, t.Week_num, t.Year, h.Hshd_num, h.Loyalty_flag, h.Age_range, h.Marital_status, h.Income_range, h.Homeowner_desc, h.Hshd_composition, h.Hshd_size, h.Children FROM products AS p LEFT JOIN transactions AS t ON p.Product_num = t.Product_num LEFT JOIN households AS h ON t.Hshd_num = h.Hshd_num ORDER BY p.Commodity LIMIT 20;""")
	return render_template("query6.html", query6=query6)	
