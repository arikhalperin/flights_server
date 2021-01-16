from app import Flight, Reservation, db
from app.main.queries.BookingDetails import extract_date


class EditBookingDetails:
    def __init__(
        self,
        destination: str = None,
        travel_date: str = None,
        unsupported_airports=None,
        capacity=0,
        user_id=-1
    ):
        if unsupported_airports is None:
            unsupported_airports = []
        self.destination = destination
        self.travel_date = travel_date
        self.unsupported_airports = unsupported_airports
        self.capacity = capacity
        self.user_id = user_id

    def variable_to_ask_for(self, value):
        self.update_previous_field_from(value)
        return self.get_next_item()

    def update_previous_field_from(self, value):
        if value is not None:
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
        if self.destination is None:
            return "to"

        if self.travel_date is None:
            return "travel_date"

        if self.capacity is None:
            return "capacity"

        if self.user_id is None:
            return "user_id"

    def finish_request(self):
        reservations = db.session.query(Reservation).filter(Flight.destination == self.destination). \
            filter(Reservation.user_id == self.user_id).all()

        the_reservation = None
        the_flight = None
        for reservation in reservations:
            flight = Flight.query.filter(Flight.id == reservation.flight_id).first()

            if self.travel_date != extract_date(flight.departure):
                continue

            the_reservation = reservation
            the_flight = flight
            break

        if the_reservation is None:
            return "no match"

        from app.api.controllers.flights_controller import modify_reservation

        body = {"reservation_id": the_reservation.id,
                "flight_id": the_flight.id,
                "number_of_seats": reservation.number_of_seats,
                "user_id": reservation.user_id}

        return modify_reservation(body)

    def to_dict(self):
        result = {
            "intent_type": "EditBooking",
            "destination": self.destination,
            "travel_date": self.travel_date,
            "capacity": self.capacity,
            "user_id": self.user_id
        }
        return result
