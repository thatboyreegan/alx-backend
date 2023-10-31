#!/usr/bin/env python3
"""A basic implemention of the flask app"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """
    an implelemtation of the flask babel configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config())


@babel.localeselector
def get_locale() -> str:
    """
    returns the timezone for a webpage
    """
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route("/")
def hello_world():
    """
    returns the home/index page
    """
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run()
