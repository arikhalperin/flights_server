import io
from datetime import timedelta, datetime

from google.cloud import speech
from google.cloud.speech_v1.proto.cloud_speech_pb2 import RecognitionAudio, RecognitionConfig
from pydub import AudioSegment

from app import Flight, db, Reservation
from app.UTILS.GCSObjectStreamUpload import GCSObjectStreamUpload


def add_flight(body):
    source = body["source"]
    destination = body["destination"]
    departure = body["departure"]
    landing = body["landing"]
    capacity = body["capacity"]
    flight = Flight(source=source, destination=destination,
                    landing=landing, departure=departure, capacity=capacity)
    db.session.add(flight)
    db.session.commit()
    return {"status": "OK"}


def remove_flight(body):
    id = body["flight_id"]
    flight = Flight.query.filter(Flight.id == id).first()
    if flight is not None:
        db.session.delete(flight)
        db.session.commit()
    return {"status": "OK"}


def modify_flight(body):
    id = body["flight_id"]
    source = body["source"]
    destination = body["destination"]
    departure = body["departure"]

    departure = datetime.strptime(departure,"%d/%m/%y %H:%M:%S")

    landing = body["landing"]
    landing = datetime.strptime(landing, "%d/%m/%y %H:%M:%S")
    capacity = body["capacity"]
    flight = Flight.query.filter(Flight.id == id).first()
    if flight is not None:
        flight.source = source
        flight.destination = destination
        flight.departure = departure
        flight.landing = landing
        flight.capacity = capacity
        db.session.commit()
    return {"status": "OK"}


def make_reservation(body):
    flight_id = body["flight_id"]
    number_of_seats = body["number_of_seats"]
    user_id = body["user_id"]
    reservation = Reservation.query.filter(Reservation.flight_id == flight_id, Reservation.user_id == user_id).first()
    if reservation is None:
        reservation = Reservation(flight_id=flight_id, user_id=user_id, number_of_seats=number_of_seats)
        flight = Flight.query.filter(Flight.id==flight_id).first()
        flight.capacity = flight.capacity-number_of_seats
        db.session.add(reservation)
        db.session.commit()
    return {"status": "OK"}


def delete_reservation(body):
    reservation_id = body["reservation_id"]

    reservation = Reservation.query.filter(Reservation.id == reservation_id).first()
    if reservation is not None:
        flight_id = reservation.flight_id
        number_of_seats = reservation.number_of_seats
        flight = Flight.query.filter(Flight.id == flight_id).first()
        flight.capacity = flight.capacity + number_of_seats
        db.session.delete(reservation)
        db.session.commit()
    return {"status": "OK"}


def modify_reservation(body):
    reservation_id = body["reservation_id"]
    flight_id = body["flight_id"]
    number_of_seats = body["number_of_seats"]
    user_id = body["user_id"]

    reservation = Reservation.query.filter(Reservation.id == reservation_id).first()
    if reservation is not None:
        flight = Flight.query.filter(Flight.id == flight_id).first()
        flight.capacity = flight.capacity + reservation.number_of_seats
        flight.capacity = flight.capacity - number_of_seats
        reservation.number_of_seats = number_of_seats
        reservation.user_id = user_id
        db.session.commit()
    return {"status": "OK"}


def get_flight_by_id(flight_id):
    flight = Flight.query.filter(Flight.id == flight_id).first()
    return flight


def format_date(departure):
    return departure.strftime("%d/%m/%y %H:%M:%S")


def get_reservations():
    reservations = Reservation.query.all()
    reservations_response = []
    for reservation in reservations:
        flight = get_flight_by_id(reservation.flight_id)

        if flight is None:
            continue

        rr = {
            "departure": format_date(flight.departure),
            "to": flight.destination,
            "id": reservation.id,
            "flight_id": reservation.flight_id,
            "number_of_seats": reservation.number_of_seats,
            "user_id": reservation.user_id
        }
        reservations_response.append(rr)
    dict = {
        "reservations": reservations_response
    }
    return dict


def get_flights(body=None):
    if body is not None:
        source = body["source"]
        destination = body["destination"]
        time = body["time"]
        number_of_seats = body["number_of_seats"]
        flights = Flight.query.filter(Flight.capacity >= number_of_seats,
                                     Flight.departure > (time-timedelta(hours=24) and Flight.departure<(time+timedelta(hours=24)),
                                     Flight.source == source, Flight.destination == destination).all())
    else:
        flights = Flight.query.all()

    flights_response = []

    for flight in flights:
        fr = {
            "id": flight.id,
            "from": flight.source,
            "to": flight.destination,
            "capacity": flight.capacity,
            "departure": flight.departure.strftime("%d/%m/%y %H:%M:%S"),
            "landing": flight.landing.strftime("%d/%m/%y %H:%M:%S")
        }
        flights_response.append(fr)
    dict= {"flights": flights_response}
    return dict

def transcribe_file(file_path):
        """Transcribe the given audio file."""
        client = speech.SpeechClient()

        with io.open(file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = RecognitionAudio(content=content)
        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            print(u"Transcript: {}".format(result.alternatives[0].transcript))


def upload(recording):
    recording.save("/tmp/recording.wav")
    order = AudioSegment.from_wav("/tmp/recording.wav")
    order.export("/tmp/recording.wav", format= "wav", bitrate="16k")
  #  f = open("/tmp/recording.wav", 'rb')

  #  with GCSObjectStreamUpload(bucket_name="flightsorderbucket", blob_name="order.wav") as s:
  #      s.write(f.read())
    transcribe_file("/tmp/recording.wav")

    response = {"status": "ok"}
    return response
