from flask import Blueprint,request

from app.controllers import PrintModelController

from app.routes.base_route import BaseRoute

class PrintModelRoute(BaseRoute):
    def __init__(self):
        print_model_bp = Blueprint("print_model",__name__)
        
        super().__init__(print_model_bp,PrintModelController())
        self.add_routes()

    def add_routes(self):

        @self._blueprint.route("/upload",methods=["POST"])
        def route_upload_file():
            return PrintModelController().controller_upload_file(request)