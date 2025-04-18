from app.models import (
    SetModel
)
from app.controllers import BaseController

class SetModelController(BaseController):
    def __init__(self):
        defaults = {
            "name": None,
            "description": None,
        }
        super().__init__(SetModel, defaults)