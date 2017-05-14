"""This module does blah blah."""
# pylint: disable=invalid-name

import logging
from models.database import Database
from intents.main import handle_intents
from flask import Flask, render_template
from flask_ask import Ask
from afg import Supervisor

app = Flask(__name__)
ask = Ask(app, "/")
sup = Supervisor("scenario.yaml")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.on_session_started
@sup.start
def new_session():
    app.logger.debug('new session started')

@sup.stop
def close_user_session():
    app.logger.debug("user session stopped")

@ask.session_ended
def session_ended():
    close_user_session()
    return "", 200

if __name__ == '__main__':
    handle_intents(ask, sup)
    app.run(debug=True)

