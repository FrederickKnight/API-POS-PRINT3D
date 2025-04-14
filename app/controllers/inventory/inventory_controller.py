from app.models import (
    Inventory
)
from app.controllers import BaseController

class InventoryController(BaseController):
    def __init__(self):
        defaults = {
            "type":None,
            "name":None,
            "description":None,
            "quantity":0,
            "quantity_type":None,
        }
        super().__init__(Inventory, defaults)