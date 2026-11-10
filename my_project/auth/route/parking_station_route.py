from flask import Blueprint, request
from my_project.auth.controller.parking_station_controller import ParkingStationController

parking_stations_bp = Blueprint('parking_stations', __name__, url_prefix='/api/parking-stations')
controller = ParkingStationController()

@parking_stations_bp.route('', methods=['GET'])
@parking_stations_bp.route('/', methods=['GET'])
def get_all_parking_stations():
    return controller.find_all()

@parking_stations_bp.route('/<int:station_id>', methods=['GET'])
def get_parking_station_by_id(station_id: int):
    return controller.find_by_id(station_id)

@parking_stations_bp.route('', methods=['POST'])
@parking_stations_bp.route('/', methods=['POST'])
def create_parking_station():
    data = request.get_json(silent=True) or {}
    return controller.create(data)

@parking_stations_bp.route('/<int:station_id>', methods=['PUT', 'PATCH'])
def update_parking_station(station_id: int):
    data = request.get_json(silent=True) or {}
    return controller.update(station_id, data)

@parking_stations_bp.route('/<int:station_id>', methods=['DELETE'])
def delete_parking_station(station_id: int):
    return controller.delete(station_id)

@parking_stations_bp.route('/<int:station_id>/retail-chain', methods=['GET'])
def get_station_parent_chain(station_id: int):
    return controller.find_parent_chain(station_id)
