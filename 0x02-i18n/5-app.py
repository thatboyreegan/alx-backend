#!/usr/bin/env python3
"""A basic implemention of the flask app"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict, Union

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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


def get_user() -> Union[Dict, None]:
    """
    returns the user id if it exists or None incase it does not
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """
    executes the get_user function before each request is resolved
    """
    user = get_user()
    g.user = user


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
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run()
