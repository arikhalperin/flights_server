from app import Flight, Reservation, db

def extract_date(date_value):
    month = date_value.month
    day = date_value.day
    year = date_value.year
    return f"{day}.{month}.{year}"

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
        if value is not None:
            if self.origin is None:
                self.origin = value
                return

            if self.destination is None:
                self.destination = value
                return

            if self.travel_date is None:
                self.travel_date = value
                return

            if self.capacity is None:
                self.capacity = value
                return

            if self.user_id is None:
                self.user_id = value
                return

    def get_next_item(self):
        if self.origin is None:
            return "from"

        if self.destination is None:
            return "to"

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
            if self.origin != flight.source:
                continue

            if self.destination != flight.destination:
                continue

            if self.travel_date != extract_date(flight.departure):
                continue

            if int(self.capacity) > flight.capacity:
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
