from flask import Blueprint,request

from app.controllers import TicketController

from app.routes.base_route import BaseRoute

class TicketRoute(BaseRoute):
    def __init__(self):
        ticket_bp = Blueprint("ticket",__name__)
        
        super().__init__(ticket_bp,TicketController())

        self.add_custom_routes()

    def add_custom_routes(self):

        @self._blueprint.route("/<int:id>/total", methods=["GET"])
        def route_get_ticket_total(id):
            return TicketController().controller_get_ticket_total(id=id,request=request)