from flask import make_response, request
from flask.views import MethodView

from app.api import api
from app.api.controllers.flights_controller import get_hello, get_wtf, get_name, add_numbers, sub_numbers, add_flight, \
    modify_flight, remove_flight, make_reservation, delete_reservation, modify_reservation, get_flights, \
    get_reservations

#MVC : Model View Controller
class GetHello(MethodView):
    def get(self):
        return make_response(get_hello(), 200)


class GetWtf(MethodView):
    def get(self):
        print("WTF????")
        return make_response(get_wtf(), 200)


class GetName(MethodView):
    def get(self):
        return make_response(get_name(), 200)


class Root(MethodView):
    def get(self):
        return make_response("This is Yoav's server", 200)


class DoAddition(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(add_numbers(request.json), 200)


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


class DoSubtraction(MethodView):
    def post(self, *args, **kwargs):
        print(request)
        return make_response(sub_numbers(request.json), 200)


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


get_hello_view = GetHello.as_view("hello_view")

get_wtf_view = GetWtf.as_view("wtf_view")

get_name_view = GetName.as_view("name_view")

do_addition_view = DoAddition.as_view("do_addition_view")

do_subtraction_view = DoSubtraction.as_view("do_subtraction_view")

root_view = Root.as_view("root_view")

add_flight_view = AddFlight.as_view("add_flight_view")
remove_flight_view = RemoveFlight.as_view("remove_flight_view")
modify_flight_view = ModifyFlight.as_view("modify_flight_view")

make_reservation_view = AddReservation.as_view("make_reservation_view")
delete_reservation_view = DeleteReservation.as_view("delete_reservation_view")
modify_reservation_view = ModifyReservation.as_view("modify_reservation_view")

get_flights_view = GetFlights.as_view("get_flights_view")
get_reservations_view = GetReservations.as_view("get_reservations_view")

api.add_url_rule(
    '/v1/get_hello',
    view_func=get_hello_view,
    methods=['GET'])

api.add_url_rule(
    '/v1/get_wtf',
    view_func=get_wtf_view,
    methods=['GET'])

api.add_url_rule(
    '/v1/get_name',
    view_func=get_name_view,
    methods=['GET'])

api.add_url_rule(
    '/v1/do_addition',
    view_func=do_addition_view,
    methods=['POST'])

api.add_url_rule(
    '/v1/do_subtraction',
    view_func=do_subtraction_view,
    methods=['POST'])

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

api.add_url_rule('/', view_func=root_view, methods=['GET'])
