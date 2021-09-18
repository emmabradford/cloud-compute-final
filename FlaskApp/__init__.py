from flask import Flask, render_template, request, url_for, redirect

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

@app.route('/signUp')
def signUp():
    return render_template("signUp.html")

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()
