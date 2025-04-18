from app.models import (
    BrandModel
)
from app.controllers import BaseController

class BrandModelController(BaseController):
    def __init__(self):
        defaults = {
            "name": None,
            "description": None,
        }
        super().__init__(BrandModel, defaults)