"""Handle intents"""



from intents.place_intents import handle_place_intents
from intents.app_intents import handle_app_intents
from intents.date_intents import handle_date_intents
from intents.moreinfo_intents import handle_moreinfo_intents
from intents.yesno_intents import handle_yesno_intents
from intents.booking_intents import handle_booking_intents


def handle_intents(ask):
    "handle intents"

    handle_app_intents(ask)
    handle_place_intents(ask)
    handle_date_intents(ask)
    handle_moreinfo_intents(ask)
    handle_yesno_intents(ask)
    handle_booking_intents(ask)
