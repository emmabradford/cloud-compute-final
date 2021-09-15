from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Bienvenidos a mdzs!"

if __name__ == "__main__":
    app.run()
