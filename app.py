"""
Main app for site, linking Jinga templates to python functions.
Function then interact with MongoDB
"""


import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
if os.path.exists('env.py'):
    import env


app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world'


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "127.0.0.1"),
            port=int(os.environ.get("PORT", 5000)),
            debug=True)
