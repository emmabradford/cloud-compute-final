from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/signUp')
def signUp():
    return render_template("signUp.html")

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()
