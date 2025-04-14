from app.models import (
    PrintModel
)
from app.controllers import BaseController

class PrintModelController(BaseController):
    def __init__(self):
        defaults = {
            "id_subtheme": None,
            "name": None,
            "description": None,
            "url_image": None,
        }
        super().__init__(PrintModel, defaults)