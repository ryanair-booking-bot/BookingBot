"""This module does blah blah."""
# pylint: disable=invalid-name

import logging
from models.database import Database
from intents.main import handle_intents
from flask import Flask
from flask_ask import Ask

app = Flask(__name__)
ask = Ask(app, "/")
db = Database()

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

if __name__ == '__main__':
    handle_intents(ask, db)
    app.run(debug=True)
