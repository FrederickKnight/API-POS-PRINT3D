from flask import Blueprint

from app.controllers.auth import AuthUserController

from app.routes.auth.base_auth_route import BaseAuthRoute

class AuthUserRoute(BaseAuthRoute):
    def __init__(self):
        auth_user_bp = Blueprint("auth_user",__name__)
        
        super().__init__(auth_user_bp,AuthUserController())