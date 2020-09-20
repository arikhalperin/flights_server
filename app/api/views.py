from flask import make_response
from flask.views import MethodView

from app.api import api
from app.api.controllers.flights_controller import get_hello

class GetHello(MethodView):
    def get(self):
        return make_response(get_hello(), 200)

get_hello_view = GetHello.as_view("hello_view")

api.add_url_rule(
    '/v1/get_hello',
    view_func=get_hello_view,
    methods=['GET'])

