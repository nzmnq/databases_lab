from flask import Blueprint, request
from my_project.auth.controller.station_maintenance_controller import StationMaintenanceController

station_maintenances_bp = Blueprint('station_maintenances', __name__, url_prefix='/api/station-maintenances')
controller = StationMaintenanceController()


@station_maintenances_bp.route('', methods=['GET'])
@station_maintenances_bp.route('/', methods=['GET'])
def get_all_station_maintenances():
    return controller.find_all()


@station_maintenances_bp.route('/<int:maintenance_id>', methods=['GET'])
def get_station_maintenance_by_id(maintenance_id: int):
    return controller.find_by_id(maintenance_id)


@station_maintenances_bp.route('/station/<int:station_id>', methods=['GET'])
def get_station_maintenances_by_station(station_id: int):
    return controller.find_by_station(station_id)


@station_maintenances_bp.route('', methods=['POST'])
@station_maintenances_bp.route('/', methods=['POST'])
def create_station_maintenance():
    data = request.get_json(silent=True) or {}
    return controller.create(data)


@station_maintenances_bp.route('/<int:maintenance_id>', methods=['PUT', 'PATCH'])
def update_station_maintenance(maintenance_id: int):
    data = request.get_json(silent=True) or {}
    return controller.update(maintenance_id, data)


@station_maintenances_bp.route('/<int:maintenance_id>', methods=['DELETE'])
def delete_station_maintenance(maintenance_id: int):
    return controller.delete(maintenance_id)
