from flask import Blueprint

from app.controllers import ErrorSaleController

from app.routes.base_route import BaseRoute

class ErrorSaleRoute(BaseRoute):
    def __init__(self):
        error_sales_bp = Blueprint("error_sales",__name__)
        
        super().__init__(error_sales_bp,ErrorSaleController())