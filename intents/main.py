"""Handle intents"""

from intents.place_intents import handle_place_intents
from intents.app_intents import handle_app_intents

def handle_intents(ask, database):
    "handle intents"

    handle_app_intents(ask, database)
    handle_place_intents(ask, database)
