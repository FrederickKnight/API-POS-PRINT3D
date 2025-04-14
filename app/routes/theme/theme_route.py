from flask import Blueprint

from app.controllers import ThemeController

from app.routes.base_route import BaseRoute

class ThemeRoute(BaseRoute):
    def __init__(self):
        theme_bp = Blueprint("theme",__name__)
        
        super().__init__(theme_bp,ThemeController())