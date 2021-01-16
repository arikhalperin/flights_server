from flask import make_response, request
from flask.views import MethodView

from app.api import api
from app.api.controllers.flights_controller import add_flight, \
    modify_flight, remove_flight, make_reservation, delete_reservation, modify_reservation, get_flights, \
    get_reservations, upload


# MVC : Model View Controller

class AddFlight(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(add_flight(request.json), 200)


class RemoveFlight(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(remove_flight(request.json), 200)


class ModifyFlight(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(modify_flight(request.json), 200)


class AddReservation(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(make_reservation(request.json), 200)


class DeleteReservation(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(delete_reservation(request.json), 200)


class ModifyReservation(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(modify_reservation(request.json), 200)


class GetFlights(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(get_flights(request.json), 200)

    def get(self):
        return make_response(get_flights(), 200)


class GetReservations(MethodView):
    def get(self):
        return make_response(get_reservations(), 200)


class Upload(MethodView):
    def post(self):
        if request.args.get("interaction_type")=="voice":
            return make_response(upload(request.files["recording"], request.args), 200)
        else:
            return make_response(upload(request.args.get("text"), request.args), 200)


add_flight_view = AddFlight.as_view("add_flight_view")
remove_flight_view = RemoveFlight.as_view("remove_flight_view")
modify_flight_view = ModifyFlight.as_view("modify_flight_view")

make_reservation_view = AddReservation.as_view("make_reservation_view")
delete_reservation_view = DeleteReservation.as_view("delete_reservation_view")
modify_reservation_view = ModifyReservation.as_view("modify_reservation_view")

get_flights_view = GetFlights.as_view("get_flights_view")
get_reservations_view = GetReservations.as_view("get_reservations_view")

upload_view = Upload.as_view("upload_view")

api.add_url_rule(
    '/v1/add_flight',
    view_func=add_flight_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/remove_flight',
    view_func=remove_flight_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/modify_flight',
    view_func=modify_flight_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/make_reservation',
    view_func=make_reservation_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/delete_reservation',
    view_func=delete_reservation_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/modify_reservation',
    view_func=modify_reservation_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/get_flights',
    view_func=get_flights_view,
    methods=['POST', 'GET'])

api.add_url_rule(
    '/v1/get_reservations',
    view_func=get_reservations_view,
    methods=['GET'])

api.add_url_rule(
    '/v1/upload',
    view_func=upload_view,
    methods=['POST'])
