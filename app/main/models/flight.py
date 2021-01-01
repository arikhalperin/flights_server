from app import db


class Flight(db.Model):

    def __init__(self, source, destination, departure, landing, capacity):
        self.source = source
        self.destination = destination
        self.departure = departure
        self.landing = landing
        self.capacity = capacity

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(80), nullable=False)
    destination = db.Column(db.String(80), nullable=False)
    departure = db.Column(db.DateTime(), nullable=False)
    landing = db.Column(db.DateTime(), nullable=False)
    capacity = db.Column(db.Integer)
