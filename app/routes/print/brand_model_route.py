from flask import Blueprint

from app.controllers import BrandModelController

from app.routes.base_route import BaseRoute

class BrandModelRoute(BaseRoute):
    def __init__(self):
        brand_model_bp = Blueprint("brand_model",__name__)
        
        super().__init__(brand_model_bp,BrandModelController())