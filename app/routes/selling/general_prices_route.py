from flask import Blueprint

from app.controllers import GeneralPricesController

from app.routes.base_route import BaseRoute

class GeneralPricesRoute(BaseRoute):
    def __init__(self):
        general_prices_bp = Blueprint("general_prices",__name__)
        
        super().__init__(general_prices_bp,GeneralPricesController())