from flask import Blueprint
from my_project.auth.controller.vehicle_controller import VehicleController
from my_project.auth.route.crud_helper import register_crud_routes

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/api/vehicles')
controller = VehicleController()
register_crud_routes(vehicles_bp, controller)
