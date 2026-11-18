from flask import Blueprint
from my_project.auth.controller.parking_zone_controller import ParkingZoneController
from my_project.auth.route.crud_helper import register_crud_routes

parking_zones_bp = Blueprint('parking_zones', __name__, url_prefix='/api/parking-zones')
controller = ParkingZoneController()
register_crud_routes(parking_zones_bp, controller)
