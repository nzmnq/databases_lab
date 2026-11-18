from flask import Blueprint
from my_project.auth.controller.reservation_delete_log_controller import ReservationDeleteLogController
from my_project.auth.route.crud_helper import register_crud_routes

reservation_delete_logs_bp = Blueprint('reservation_delete_logs', __name__, url_prefix='/api/reservation-delete-logs')
controller = ReservationDeleteLogController()
register_crud_routes(reservation_delete_logs_bp, controller)
