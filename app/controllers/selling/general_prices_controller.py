from app.models import (
    GeneralPrices
)
from app.controllers import BaseController

class GeneralPricesController(BaseController):
    def __init__(self):
        defaults = {
            "id_material_type": None,
            "date": None,
            "wear": None,
            "electricity": None,
            "margin": None,
            "failure_risk": {"low": 0.0, "medium": 0.0, "high": 0.0},
            "formula": None,
        }
        super().__init__(GeneralPrices, defaults)