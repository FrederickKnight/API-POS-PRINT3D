from .base_auth_controller import BaseAuthController

from app.models import (
    User,
    Session
)

class AuthUserController(BaseAuthController):
    def __init__(self):
        user_defaults = {
        "username": None,
        "password": None,
        "is_active": True,
        "auth_level": None,
        }

        session_defaults = {
            "id_user": None,
            "session": None,
            "expires_at": None
        }
        super().__init__(User, user_defaults, Session, session_defaults)