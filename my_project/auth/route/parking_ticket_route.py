from flask import Blueprint
from my_project.auth.controller.parking_ticket_controller import ParkingTicketController
from my_project.auth.route.crud_helper import register_crud_routes

parking_tickets_bp = Blueprint('parking_tickets', __name__, url_prefix='/api/parking-tickets')
controller = ParkingTicketController()
register_crud_routes(parking_tickets_bp, controller)
