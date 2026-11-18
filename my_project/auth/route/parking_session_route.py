from flask import Blueprint
from my_project.auth.controller.parking_session_controller import ParkingSessionController
from my_project.auth.route.crud_helper import register_crud_routes

parking_sessions_bp = Blueprint('parking_sessions', __name__, url_prefix='/api/parking-sessions')
controller = ParkingSessionController()
register_crud_routes(parking_sessions_bp, controller)
