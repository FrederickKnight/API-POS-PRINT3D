from flask import Blueprint

from app.controllers import SetModelController

from app.routes.base_route import BaseRoute

class SetModelRoute(BaseRoute):
    def __init__(self):
        set_model_bp = Blueprint("set_model",__name__)
        
        super().__init__(set_model_bp,SetModelController())