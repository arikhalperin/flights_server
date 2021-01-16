from app import db


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer)
    number_of_seats = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(32), nullable=False)

    def __init__(self,flight_id, number_of_seats, user_id):
        self.flight_id = flight_id
        self.number_of_seats = number_of_seats
        self.user_id = user_id
