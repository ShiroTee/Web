from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from auth import auth
from main import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.register_blueprint(auth)
app.register_blueprint(main)

moment = Moment(app)


if __name__ == '__main__':
    app.run(debug=True)