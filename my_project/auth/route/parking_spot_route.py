from flask import Blueprint
from my_project.auth.controller.parking_spot_controller import ParkingSpotController
from my_project.auth.route.crud_helper import register_crud_routes

parking_spots_bp = Blueprint('parking_spots', __name__, url_prefix='/api/parking-spots')
controller = ParkingSpotController()
register_crud_routes(parking_spots_bp, controller)
