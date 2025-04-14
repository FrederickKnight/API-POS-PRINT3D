from flask import Blueprint,request
from app.controllers.auth.base_auth_controller import BaseAuthController

class BaseAuthRoute:
    def __init__(self,blueprint:Blueprint,controller:BaseAuthController):
        self._blueprint = blueprint
        self._controller = controller
        
        self._create_routes()
        
    def _create_routes(self):
        
        @self._blueprint.route("/register",methods=["POST"])
        def route_register_user():
            json_request = request.get_json()
            return self._controller.register_user(json_request)

        @self._blueprint.route("/<int:id>/search",methods=["GET"])
        def route_get_by_id_user(id):
            return self._controller.get_by_id(id)

        @self._blueprint.route("/user-validation",methods=["POST"])
        def route_user_validation_user():
            json_request = request.get_json()
            return self._controller.validate_user(json_request)

        @self._blueprint.route("/<int:id>/delete",methods=["DELETE"])
        def route_delete_by_id(id):
            return self._controller.delete_user_by_id(id)

        @self._blueprint.route("/session-token",methods=["GET"])
        def route_session_token():
            return self._controller.generateSessionToken()

        @self._blueprint.route("/create-session/<int:id>",methods=["POST"])
        def route_test_user(id):
            json_request = request.get_json()
            return self._controller.createSessionToken(json_request,id)

        @self._blueprint.route("/session-validation",methods=["POST"])
        def route_test_validation_user():
            json_request = request.get_json()
            return self._controller.validateSessionToken(json_request["token"])

        @self._blueprint.route("/session-invalidation",methods=["POST"])
        def route_test_invalidation_user():
            json_request = request.get_json()
            return self._controller.invalidateSession(json_request["session"])
        
    def get_blueprint(self):
        return self._blueprint