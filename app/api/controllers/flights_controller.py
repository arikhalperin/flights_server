import io
import json
from datetime import timedelta, datetime

from google.cloud import speech
from google.cloud.speech_v1.proto.cloud_speech_pb2 import RecognitionAudio, RecognitionConfig
from pydub import AudioSegment

from app import Flight, db, Reservation
from app.UTILS.GCSObjectStreamUpload import GCSObjectStreamUpload
from app.UTILS.get_luis_result import get_luis_result
from app.main.queries.BookingDetails import BookingDetails
from app.main.queries.CancelBookingDetails import CancelBookingDetails
from app.main.queries.EditBookingDetails import EditBookingDetails


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

    departure = datetime.strptime(departure, "%d/%m/%y %H:%M:%S")

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
        flight = Flight.query.filter(Flight.id == flight_id).first()
        flight.capacity = flight.capacity - number_of_seats
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
                                      Flight.departure > (
                                      time - timedelta(hours=24) and Flight.departure < (time + timedelta(hours=24)),
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
    dict = {"flights": flights_response}
    return dict


def transcribe_file(file_path):
    """Transcribe the given audio file."""
    print("transcribing")
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    print("Opended file")
    audio = RecognitionAudio(content=content)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    print("Calling google recognize")
    response = client.recognize(config=config, audio=audio)
    print("Got response")
    print(response)

    if len(response.results)==0 or len(response.results[0].alternatives)==0:
        return None

    result = response.results[0].alternatives[0].transcript

    result = result.strip().lower()

    return result
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    # for result in response.results:
    #    # The first alternative is the most likely one for this portion.
    #    print(u"Transcript: {}".format(result.alternatives[0].transcript))


def parse_intent_from_args(data):
    intent_type = data["intent_type"]
    if intent_type == "BookFlight":
        origin = None
        destination = None
        flight_date = None
        capacity = None
        user_id = None

        if "origin" in data:
            origin = data["origin"]

        if "destination" in data:
            destination = data["destination"]

        if "travel_date" in data:
            flight_date = data["travel_date"]

        if "capacity" in data:
            capacity = data["capacity"]

        if "user_id" in data:
            user_id = data["user_id"]

        return BookingDetails(origin=origin, destination=destination,
                              travel_date=flight_date, capacity=capacity, user_id=user_id)

    if intent_type == "CancelBooking":
        destination = None
        flight_date = None
        user_id = None

        if "destination" in data:
            destination = data["destination"]

        if "travel_date" in data:
            flight_date = data["travel_date"]

        if "user_id" in data:
            user_id = data["user_id"]

        return CancelBookingDetails(destination=destination, travel_date=flight_date, user_id=user_id)

    if intent_type == "EditBooking":
        destination = None
        flight_date = None
        capacity = None
        user_id = None

        if "destination" in data:
            destination = data["destination"]

        if "travel_date" in data:
            flight_date = data["travel_date"]

        if "capacity" in data:
            capacity = int(data["capacity"])

        if "user_id" in data:
            user_id = str(int(data["user_id"]))

        return EditBookingDetails(destination=destination,
                              travel_date=flight_date, capacity=capacity, user_id=user_id)


def upload(recording, args):
    if args.get("interaction_type") == "voice":
        recording.save("/tmp/recording.wav")
        text = transcribe_file("/tmp/recording.wav")
    else:
        text = recording

    data = args.get("data")

    if data is None:
        result = get_luis_result(text)
        text = "LUIS RESULT"
    else:
        print(f"Got data:{data}")
        data = json.loads(data)
        result = parse_intent_from_args(data)
    try:
        if text is None or text == "":
            raise Exception()
        next = result.variable_to_ask_for(text)
        if next is None:
            status = result.finish_request()
            print(f"Status is:{status}")
            response = {"status": status}
        else:
            response = {
                "status": "more_data",
                "data": result.to_dict(),
                "next": next}
            print(f"Response is {response}")
    except Exception as e:
        print(str(e))
        response = {
            "status": "more_data",
            "data": data,
            "next": result.get_next_item()}
    return response
