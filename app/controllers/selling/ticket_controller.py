from app.models import (
    Ticket,
)
from app.controllers import BaseController

from flask import Response,Request

class TicketController(BaseController):
    def __init__(self):
        defaults = {
            "id_client": None,
            "id_user": None,
            "date": None,
            "subject": None,
        }
        super().__init__(Ticket, defaults)

    

    def controller_get_ticket_total(self,id,request:Request):
        version = request.headers.get("Accept")
        ticket = self.__query_args__(request.args,id)

        if isinstance(ticket,Response):
            return self.__return_json__(ticket,version)
        
        # si se encontro ticket despues de revisar los argumentos
        # obtener el ticket y obtener el total aunque se esta haciendo la query 2 veces
        # Mejorar despues

        id_ticket = ticket[0].get("id",None)
        res_ticket = self.session.query(Ticket).get(id_ticket)
        total = res_ticket.get_total()

        return self.__return_json__({"id":id_ticket,"total":total},version)