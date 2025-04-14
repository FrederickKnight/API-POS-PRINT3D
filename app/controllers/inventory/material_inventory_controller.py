from app.models import (
    MaterialInventory
)
from app.controllers import BaseController

class MaterialInventoryController(BaseController):
    def __init__(self):
        defaults = {
            "id_material":None,
            "quantity":0,
        }
        super().__init__(MaterialInventory, defaults)