from app import db


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer)
    number_of_seats = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(32), nullable=False)

