from datetime import datetime, timedelta
from typing import Any, Tuple
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from my_project import db
from my_project.auth.controller.general_controller import GeneralController, extract_db_error_message
from my_project.auth.domain.parking_reservation import ParkingReservation
from my_project.auth.service.parking_reservation_service import ParkingReservationService


class ParkingReservationController(GeneralController):
    _service = ParkingReservationService()

    def create(self) -> Tuple[Any, int]:
        data = request.get_json(silent=True) or {}
        client_id = data.get('client_id')
        spot_id = data.get('spot_id')

        if client_id is None or spot_id is None:
            return {'error': 'Both client_id and spot_id are required'}, 400

        if self._service.get_client(client_id) is None:
            return {'error': f'Client with id={client_id} does not exist'}, 400

        if self._service.get_spot(spot_id) is None:
            return {'error': f'ParkingSpot with id={spot_id} does not exist'}, 400

        now = datetime.utcnow()
        payload = {
            'client_id': client_id,
            'spot_id': spot_id,
            'license_plate': data.get('license_plate') or 'BC0000AA',
            'reserved_from': data.get('reserved_from') or now,
            'reserved_to': data.get('reserved_to') or (now + timedelta(hours=2)),
            'booking_fee': data.get('booking_fee', 0.00),
            'status': data.get('status', 'CONFIRMED'),
        }

        try:
            reservation = ParkingReservation.create_from_dto(payload)
        except ValueError as err:
            return {'error': f'Invalid datetime format: {err}'}, 400

        try:
            created = self._service.create(reservation)
        except SQLAlchemyError as err:
            db.session.rollback()
            return {
                'error': 'Database Trigger / Integrity Error',
                'details': extract_db_error_message(err),
            }, 400
        return created.put_into_dto(), 201

    def find_spots_by_client(self, client_id: int) -> Tuple[Any, int]:
        client = self._service.get_client(client_id)
        if client is None:
            return {'error': f'Client with id={client_id} not found'}, 404
        return {
            'client': client.put_into_dto(),
            'reserved_spots': [spot.put_into_dto() for spot in client.reserved_spots],
        }, 200

    def find_clients_by_spot(self, spot_id: int) -> Tuple[Any, int]:
        spot = self._service.get_spot(spot_id)
        if spot is None:
            return {'error': f'ParkingSpot with id={spot_id} not found'}, 404
        return {
            'parking_spot': spot.put_into_dto(),
            'reserving_clients': [client.put_into_dto() for client in spot.reserving_clients],
        }, 200

    def find_grouped_by_clients(self) -> Tuple[Any, int]:
        return self._service.get_grouped_by_clients(), 200
