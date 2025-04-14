from flask import Blueprint

from app.controllers import MaterialInventoryController

from app.routes.base_route import BaseRoute

class MaterialInventoryRoute(BaseRoute):
    def __init__(self):
        material_inventory_bp = Blueprint("material_inventory",__name__)
        
        super().__init__(material_inventory_bp,MaterialInventoryController())