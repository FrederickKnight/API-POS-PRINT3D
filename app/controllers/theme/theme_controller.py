from app.models import (
    Theme
)
from app.controllers import BaseController

class ThemeController(BaseController):
    def __init__(self):
        defaults = {
            "name":None,
            "description":None,
        }
        super().__init__(Theme, defaults)