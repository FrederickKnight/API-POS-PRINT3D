from flask import Blueprint

from app.controllers import InventoryController

from app.routes.base_route import BaseRoute

class InventoryRoute(BaseRoute):
    def __init__(self):
        inventory_bp = Blueprint("inventory",__name__)
        
        super().__init__(inventory_bp,InventoryController())