from flask import Blueprint

from app.controllers import SalesController

from app.routes.base_route import BaseRoute

class SalesRoute(BaseRoute):
    def __init__(self):
        sales_bp = Blueprint("sales",__name__)
        
        super().__init__(sales_bp,SalesController())