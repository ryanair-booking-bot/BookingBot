"""Handle intents"""



from intents.place_intents import handle_place_intents
from intents.app_intents import handle_app_intents
from intents.date_intents import handle_date_intents
from intents.time_intents import handle_time_intents
from intents.moreinfo_intents import handle_moreinfo_intents
from intents.yesno_intents import handle_yesno_intents
from intents.booking_intents import handle_booking_intents


def handle_intents(ask, sup):
    "handle intents"

    handle_app_intents(ask, sup)
    handle_place_intents(ask, sup)
    handle_date_intents(ask, sup)
    handle_time_intents(ask, sup)
    handle_moreinfo_intents(ask, sup)
    handle_yesno_intents(ask, sup)
    handle_booking_intents(ask, sup)
