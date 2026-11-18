from typing import Any, Dict, Tuple
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from my_project import db
from my_project.auth.controller.general_controller import GeneralController, extract_db_error_message
from my_project.auth.domain.station_maintenance import StationMaintenance
from my_project.auth.service.station_maintenance_service import StationMaintenanceService


class StationMaintenanceController(GeneralController):
    def __init__(self):
        self._service = StationMaintenanceService()

    def create(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        station_id = data.get('station_id')
        inspector_code = data.get('inspector_code')
        description = data.get('description')

        if station_id is None or not inspector_code or not description:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['station_id', 'inspector_code', 'description'],
            }), 400

        try:
            entity = StationMaintenance.create_from_dto(data)
        except ValueError as err:
            return jsonify({'error': f'Invalid datetime format: {err}'}), 400

        try:
            created = self._service.create(entity)
        except SQLAlchemyError as err:
            db.session.rollback()
            return jsonify({
                'error': 'Database Trigger / Integrity Error',
                'details': extract_db_error_message(err),
            }), 400

        return jsonify(created.put_into_dto()), 201

    def update(self, entity_id: int, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        existing = self._service.get_by_id(entity_id)
        if not existing:
            return jsonify({'error': 'Station maintenance not found', 'id': entity_id}), 404

        try:
            updated = self._service.update(entity_id, data)
        except SQLAlchemyError as err:
            db.session.rollback()
            return jsonify({
                'error': 'Database Trigger / Integrity Error',
                'details': extract_db_error_message(err),
            }), 400

        return jsonify(updated.put_into_dto()), 200

    def find_by_station(self, station_id: int) -> Tuple[Any, int]:
        items = self._service.get_by_station_id(station_id)
        return jsonify({
            'station_id': station_id,
            'total_maintenances': len(items),
            'maintenances': [item.put_into_dto() for item in items],
        }), 200
