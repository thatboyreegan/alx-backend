#!/usr/bin/env python3
"""A basic implemention of the flask app"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    """
    returns the home/index page
    """
    return render_template("0-index.html")


if __name__ == "__name__":
    app.run()
