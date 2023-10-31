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
    queries = request.query_string.decode('utf-8').split('&')
    query = dict(map(
        lambda x: (x if '=' in x else f'{x}=').split('='), queries
    ))
    if 'locale' in query:
        if query['locale'] in Config.LANGUAGES:
            return query['locale']
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route("/")
def hello_world():
    """
    returns the home/index page
    """
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run()
