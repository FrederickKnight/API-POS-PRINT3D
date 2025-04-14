from app.models import (
    Sales
)
from app.controllers import BaseController

class SalesController(BaseController):
    def __init__(self):
        defaults = {
            "id_ticket": None,
            "id_print_model": None,
            "id_general_price": None,
            "material_quantity": None,
            "print_time": None,
            "risk": None,
            "discount": None,
        }
        super().__init__(Sales, defaults)