from flask import Flask, render_template, flash, request, url_for, redirect, session
from dbconnect import connection
from wtforms import Form
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc


app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def homepage():
    error = ''
    try:        
        if request.method == "POST":	
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('info'))
				
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
    

@app.route('/signUp')
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
        return render_template("signUp.html", form=from)
    except Exception as e:
        return(str(e))

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()
