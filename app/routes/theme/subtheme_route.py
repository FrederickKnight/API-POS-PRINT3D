from flask import Blueprint

from app.controllers import SubthemeController

from app.routes.base_route import BaseRoute

class SubthemeRoute(BaseRoute):
    def __init__(self):
        subtheme_bp = Blueprint("subtheme",__name__)
        
        super().__init__(subtheme_bp,SubthemeController())