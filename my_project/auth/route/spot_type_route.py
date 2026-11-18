from flask import Blueprint
from my_project.auth.controller.spot_type_controller import SpotTypeController
from my_project.auth.route.crud_helper import register_crud_routes

spot_types_bp = Blueprint('spot_types', __name__, url_prefix='/api/spot-types')
controller = SpotTypeController()
register_crud_routes(spot_types_bp, controller)
