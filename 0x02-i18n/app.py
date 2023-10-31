#!/usr/bin/env python3
"""A basic implemention of the flask app"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict, Union
import pytz

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config())


def get_user() -> Union[Dict, None]:
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    locale = request.args.get('locale', '')
    if locale in Config.LANGUAGES:
        return locale
    if g.user and g.user['locale'] in Config.LANGUAGES:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in Config.LANGUAGES:
        return header_locale
    return Config.BABEL_DEFAULT_LOCALE


@babel.timezoneselector
def get_timezone() -> str:
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return Config.BABEL_DEFAULT_TIMEZONE


@app.route("/")
def hello_world():
    return render_template("7-index.html")


if __name__ == "__main__":
    app.run()
