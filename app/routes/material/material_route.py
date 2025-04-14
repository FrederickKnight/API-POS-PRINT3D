from flask import Blueprint

from app.controllers import MaterialController

from app.routes.base_route import BaseRoute

class MaterialRoute(BaseRoute):
    def __init__(self):
        material_bp = Blueprint("material",__name__)
        
        super().__init__(material_bp,MaterialController())