from app.custom_errors import (
    AttributeError,
    VersionError,
    InvalidIDError
)

from app.controllers.versions import (
    JsonResponseV1
)

import json
import re

from functools import wraps
from flask import request,Response

from app import db
from app.models import (
    User,
    Session
)
from app.controllers.auth import AuthUserController

session = db.session
auth_controller = AuthUserController()

def requires_auth(auth_levels:list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            cookies = request.cookies
            c_session = cookies.get("session")

            try:
                result = auth_controller.validateSessionToken(c_session)
                result_json = json.loads(result.response[0])
                user = session.query(User).filter_by(id = result_json["user"]["id"]).first()

                if user.check_auth_level(auth_levels):
                    return func(*args,**kwargs)
                else:
                    return Response(status=401)

            except Exception as e:
                print(e)
                return Response(status=401)

        return wrapper
    return decorator