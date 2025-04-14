from flask import Blueprint

from app.controllers import PrintModelController

from app.routes.base_route import BaseRoute

class PrintModelRoute(BaseRoute):
    def __init__(self):
        print_model_bp = Blueprint("print_model",__name__)
        
        super().__init__(print_model_bp,PrintModelController())