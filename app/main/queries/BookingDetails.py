from dateutil.parser import parse

from app import Flight, Reservation, db
from app.UTILS.StringUtils import convert_number, compare_date


def extract_date(date_value):
    print(f"Extracting date:{date_value}")
    month = date_value.month
    day = date_value.day
    year = date_value.year
    result = f"{day}.{month}.{year}"


class BookingDetails:
    def __init__(
            self,
            destination: str = None,
            origin: str = None,
            travel_date: str = None,
            unsupported_airports=None,
            capacity=0,
            user_id=-1
    ):
        if unsupported_airports is None:
            unsupported_airports = []
        self.destination = destination
        self.origin = origin
        self.travel_date = travel_date
        self.unsupported_airports = unsupported_airports
        self.capacity = capacity
        self.user_id = user_id

    def variable_to_ask_for(self, value):
        self.update_previous_field_from(value)
        return self.get_next_item()

    def update_previous_field_from(self, value):
        if value != "LUIS RESULT":
            print(f"Got value:{value}")
            if self.origin is None:
                print("setting origin")
                self.origin = value.lower()
                return

            if self.destination is None:
                print("setting destination")
                self.destination = value.lower()
                return

            if self.travel_date is None:
                self.travel_date = parse(value)
                return

            if self.capacity is None:
                print("setting capacity")
                self.capacity = convert_number(value)
                return

            if self.user_id is None:
                print("setting userid")
                self.user_id = str(int(value))
                return
        else:
            print("This is the LUIS result")

    def get_next_item(self):
        if self.origin is None:
            return "origin"

        if self.destination is None:
            return "destination"

        if self.travel_date is None:
            return "travel_date"

        if self.capacity is None:
            return "capacity"

        if self.user_id is None:
            return "user_id"

    def finish_request(self):
        flights = Flight.query.all()

        the_flight = None
        for flight in flights:
            if self.origin.lower() != flight.source.lower():
                print(f"No match on origin:{self.origin}")
                continue

            if self.destination.lower() != flight.destination.lower():
                print(f"No match on destination:{self.destination}")
                continue

            if not compare_date(self.travel_date,flight.departure):
                print(f"No match on date:{self.travel_date}")
                continue

            if int(self.capacity) > flight.capacity:
                print(f"Too big a capacity:{self.capacity}")
                continue

            the_flight = flight
            break

        if the_flight is None:
            return "no match"

        from app.api.controllers.flights_controller import make_reservation
        body = {"flight_id": the_flight.id,"number_of_seats": self.capacity,"user_id": self.user_id}
        return make_reservation(body)


    def to_dict(self):
        result = {
            "intent_type": "BookFlight",
            "origin": self.origin,
            "destination": self.destination,
            "travel_date": self.travel_date,
            "capacity": self.capacity,
            "user_id": self.user_id
        }
        return result
