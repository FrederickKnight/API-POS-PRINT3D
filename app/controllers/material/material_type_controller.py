from app.models import (
    MaterialType
)
from app.controllers import BaseController

class MaterialTypeController(BaseController):
    def __init__(self):
        defaults = {
            "name": None
        }
        super().__init__(MaterialType, defaults)