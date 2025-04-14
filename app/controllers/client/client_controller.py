from app.models import (
    Client
)
from app.controllers import BaseController

class ClientController(BaseController):
    def __init__(self):
        defaults = {
            "name": None,
            "email": None,
            "telephone": None,
            "address":None
        }
        super().__init__(Client, defaults)