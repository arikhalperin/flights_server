from dateutil.parser import parse

from app import Flight, Reservation, db
from app.UTILS.StringUtils import compare_date
from app.main.queries.BookingDetails import extract_date


class CancelBookingDetails:
    def __init__(
        self,
        destination: str = None,
        travel_date: str = None,
        unsupported_airports=None,
        user_id=-1
    ):
        if unsupported_airports is None:
            unsupported_airports = []
        self.destination = destination
        self.travel_date = travel_date
        self.unsupported_airports = unsupported_airports
        self.user_id = user_id

    def variable_to_ask_for(self, value):
        self.update_previous_field_from(value)
        return self.get_next_item()

    def update_previous_field_from(self, value):
        if value != "LUIS RESULT":
            print(f"Got value:{value}")
            if self.destination is None:
                print("setting destination")
                self.destination = value.lower()
                return

            if self.travel_date is None:
                self.travel_date = parse(value)
                return

            if self.user_id is None:
                print("setting userid")
                self.user_id = str(int(value))
                return
        else:
            print("This is the LUIS result")

    def get_next_item(self):
        if self.destination is None:
            return "to"

        if self.travel_date is None:
            return "travel_date"

        if self.user_id is None:
            return "user_id"

    def finish_request(self):
        reservations = db.session.query(Reservation).filter(Flight.destination==self.destination).\
            filter(Reservation.user_id == self.user_id).all()

        the_reservation = None
        for reservation in reservations:
            flight = Flight.query.filter(Flight.id == reservation.flight_id).first()

            if not compare_date(self.travel_date, flight.departure):
                print(f"No match on date:{self.travel_date}")
                continue

            if self.destination.lower() != flight.destination.lower():
                print(f"No match on destination:{self.destination}")
                continue

            if not compare_date(self.travel_date,flight.departure):
                print(f"No match on date:{self.travel_date}")
                continue

            the_reservation = reservation
            break

        if the_reservation is None:
            return "no match"

        from app.api.controllers.flights_controller import delete_reservation
        body = {"reservation_id": the_reservation.id}
        return delete_reservation(body)

    def to_dict(self):
        result = {
            "intent_type": "CancelBooking",
            "destination": self.destination,
            "travel_date": self.travel_date,
            "user_id": self.user_id
        }
        return result
