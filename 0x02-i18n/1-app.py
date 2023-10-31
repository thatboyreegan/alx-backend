#!/usr/bin/env python3
"""A basic implemention of the flask app"""

from flask import Flask, render_template
from flask_babel import Babel
from pytz import utc


app = Flask(__name__)

babel = Babel(app)


class Config:
    """
    an implelemtation of the flask babel configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config())


@app.route("/")
def hello_world() -> str:
    """
    returns the home/index page
    """
    return render_template("1-index.html")


if __name__ == "__name__":
    app.run()
