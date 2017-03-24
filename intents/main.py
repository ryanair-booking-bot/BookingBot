"""Handle intents"""

from intents.place_intents import handle_place_intents
from intents.app_intents import handle_app_intents

def handle_intents(ask):
    "handle intents"

    handle_app_intents(ask)
    handle_place_intents(ask)
