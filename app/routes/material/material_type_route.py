from flask import Blueprint

from app.controllers import MaterialTypeController

from app.routes.base_route import BaseRoute

class MaterialTypeRoute(BaseRoute):
    def __init__(self):
        material_type_bp = Blueprint("material_type",__name__)
        
        super().__init__(material_type_bp,MaterialTypeController())