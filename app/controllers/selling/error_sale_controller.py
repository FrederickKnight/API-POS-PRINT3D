from app.models import (
    ErrorSale
)
from app.controllers import BaseController

class ErrorSaleController(BaseController):
    def __init__(self):
        defaults = {
            "id_sale":None,
            "waste":None,
            "reajusted_price":None,
            "description":None,
        }
        super().__init__(ErrorSale, defaults)