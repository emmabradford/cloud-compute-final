from flask import Flask, render_template, flash, request, url_for, redirect
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    try:
        
        return render_template("main.html")
    except Exception as e:
        return render_template("main.html")

@app.route('/signUp')
def signUp():
    return render_template("signUp.html")

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()
