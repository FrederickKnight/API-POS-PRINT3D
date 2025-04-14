from app.models import (
    Subtheme
)
from app.controllers import BaseController

class SubthemeController(BaseController):
    def __init__(self):
        defaults = {
            "name":None,
            "description":None,
            "id_theme":None,
        }
        super().__init__(Subtheme, defaults)