from flask import Response,Request,json
from werkzeug.utils import secure_filename
import os
from pathlib import Path

from app import app

from app.models import (
    PrintModel
)
from app.controllers import BaseController

from app.custom_errors import (
    InvalidFile
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',"webp"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class PrintModelController(BaseController):
    def __init__(self):
        defaults = {
            "id_subtheme": None,
            "name": None,
            "description": None,
            "url_image": None,
        }
        super().__init__(PrintModel, defaults)

    def controller_upload_file(self,request:Request):
        if "file" not in request.files:
            raise InvalidFile("There is no file in given data")
        
        file = request.files["file"]

        if file.filename == "":
            raise InvalidFile("There is no selected File")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = Path(app.config["UPLOAD_FOLDER"]) / "print_models" / filename
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(str(filepath))
            return Response(response=json.dumps({"path":f"{str(filepath)}"}),status=201)
        
        return Response(status=402)