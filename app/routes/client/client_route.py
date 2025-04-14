from flask import Blueprint

from app.controllers import ClientController

from app.routes.base_route import BaseRoute

class ClientRoute(BaseRoute):
    def __init__(self):
        client_bp = Blueprint("client",__name__)
        
        super().__init__(client_bp,ClientController())