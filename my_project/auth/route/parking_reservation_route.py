from flask import Blueprint, jsonify
from my_project.auth.controller.parking_reservation_controller import ParkingReservationController

parking_reservations_bp = Blueprint('parking_reservations', __name__, url_prefix='/api/reservations')
controller = ParkingReservationController()


@parking_reservations_bp.route('', methods=['GET'])
def get_all_reservations():
    return controller.find_all()


@parking_reservations_bp.route('/<int:reservation_id>', methods=['GET'])
def get_reservation_by_id(reservation_id: int):
    return controller.find_by_id(reservation_id)


@parking_reservations_bp.route('', methods=['POST'])
def create_reservation():
    result, status = controller.create()
    return jsonify(result), status


@parking_reservations_bp.route('/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id: int):
    return controller.delete(reservation_id)


@parking_reservations_bp.route('/grouped-by-clients', methods=['GET'])
def get_reservations_grouped_by_clients():
    result, status = controller.find_grouped_by_clients()
    return jsonify(result), status


@parking_reservations_bp.route('/clients/<int:client_id>/spots', methods=['GET'])
def get_spots_by_client(client_id: int):
    result, status = controller.find_spots_by_client(client_id)
    return jsonify(result), status


@parking_reservations_bp.route('/spots/<int:spot_id>/clients', methods=['GET'])
def get_clients_by_spot(spot_id: int):
    result, status = controller.find_clients_by_spot(spot_id)
    return jsonify(result), status
