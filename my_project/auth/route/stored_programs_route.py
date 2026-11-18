from flask import Blueprint, request
from my_project.auth.controller.stored_programs_controller import StoredProgramsController

stored_programs_bp = Blueprint('stored_programs', __name__, url_prefix='/api/stored-programs')
controller = StoredProgramsController()


@stored_programs_bp.route('/station-maintenances', methods=['POST'])
def sp_insert_station_maintenance():
    data = request.get_json(silent=True) or {}
    return controller.insert_station_maintenance(data)


@stored_programs_bp.route('/reservations-m2m', methods=['POST'])
def sp_create_reservation_m2m():
    data = request.get_json(silent=True) or {}
    return controller.create_reservation_m2m(data)


@stored_programs_bp.route('/noname-batch', methods=['POST'])
def sp_insert_noname_batch():
    data = request.get_json(silent=True) or {}
    return controller.insert_noname_batch(data)


@stored_programs_bp.route('/station-stats', methods=['GET'])
def sp_get_station_rate_stats():
    return controller.get_station_rate_stats()


@stored_programs_bp.route('/cursor-split', methods=['POST'])
def sp_split_clients_cursor():
    return controller.split_clients_cursor()


@stored_programs_bp.route('/audit-logs', methods=['GET'])
def get_reservation_delete_logs():
    return controller.get_delete_logs()
