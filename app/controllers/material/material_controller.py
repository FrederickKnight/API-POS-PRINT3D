from app.models import (
    Material
)
from app.controllers import BaseController

class MaterialController(BaseController):
    def __init__(self):
        defaults = {
            "name":None,
            "brand":None,
            "measurement_type":None,
            "color":None,
            "id_material_type":None,
        }
        super().__init__(Material, defaults)