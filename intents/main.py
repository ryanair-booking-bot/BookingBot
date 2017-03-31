"""Handle intents"""

from intents.place_intents import handle_place_intents
from intents.app_intents import handle_app_intents
from intents.date_intents import handle_date_intents

def handle_intents(ask):
    "handle intents"

    handle_app_intents(ask)
    handle_place_intents(ask)
    handle_date_intents(ask)
