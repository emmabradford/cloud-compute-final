from flask import Flask, render_template, request, url_for, redirect
from dbconnect import connection

app = Flask(__name__)

@app.route('/', methods-['GET', 'POST'])
def homepage():
     error = ''
    try:

        if request.method == "POST":

            attempted_username = request.form['uname']
            attempted_password = request.form['psw']

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('info'))

            else:
                error = "Invalid credentials. Try Again."

        return render_template("main.html", error = error)

    except Exception as e:
        return render_template("main.html", error = error)

@app.route('/signUp',  methods-['GET', 'POST'])
def signUp():
    try:
        c, conn = connection()
        return render_template("signUp.html")
    except Exception as e:
        return(str(e))

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()
