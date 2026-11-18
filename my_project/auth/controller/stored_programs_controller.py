from datetime import datetime, timedelta
from typing import Any, Dict, Tuple
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from my_project import db
from my_project.auth.controller.general_controller import extract_db_error_message
from my_project.auth.service.stored_programs_service import StoredProgramsService


class StoredProgramsController:
    def __init__(self):
        self._service = StoredProgramsService()

    @staticmethod
    def _db_error_response(err: SQLAlchemyError) -> Tuple[Any, int]:
        db.session.rollback()
        return jsonify({
            'error': 'Database Trigger / Procedure Error',
            'details': extract_db_error_message(err),
        }), 400

    def insert_station_maintenance(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        station_id = data.get('station_id')
        inspector_code = data.get('inspector_code')
        description = data.get('description')
        maintenance_cost = data.get('maintenance_cost', 0.00)

        if station_id is None or not inspector_code or not description:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['station_id', 'inspector_code', 'description'],
            }), 400

        try:
            created = self._service.insert_station_maintenance(
                station_id=int(station_id),
                inspector_code=str(inspector_code),
                description=str(description),
                maintenance_cost=float(maintenance_cost),
            )
        except (ValueError, TypeError) as err:
            return jsonify({'error': f'Invalid parameter value: {err}'}), 400
        except SQLAlchemyError as err:
            return self._db_error_response(err)

        return jsonify({
            'message': 'Inserted via stored procedure sp_insert_station_maintenance',
            'data': created,
        }), 201

    def create_reservation_m2m(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        client_email = data.get('client_email')
        spot_number = data.get('spot_number')

        if not client_email or not spot_number:
            return jsonify({
                'error': 'Both client_email and spot_number are required',
                'required': ['client_email', 'spot_number'],
            }), 400

        now = datetime.utcnow()
        reserved_from_raw = data.get('reserved_from')
        reserved_to_raw = data.get('reserved_to')

        try:
            reserved_from = (
                datetime.fromisoformat(reserved_from_raw)
                if isinstance(reserved_from_raw, str)
                else (reserved_from_raw or now)
            )
            reserved_to = (
                datetime.fromisoformat(reserved_to_raw)
                if isinstance(reserved_to_raw, str)
                else (reserved_to_raw or (now + timedelta(hours=2)))
            )
            booking_fee = float(data.get('booking_fee', 0.00))
        except (ValueError, TypeError) as err:
            return jsonify({'error': f'Invalid parameter format: {err}'}), 400

        try:
            created = self._service.create_reservation_by_values(
                client_email=str(client_email),
                spot_number=str(spot_number),
                license_plate=str(data.get('license_plate') or 'BC0000AA'),
                reserved_from=reserved_from.strftime('%Y-%m-%d %H:%M:%S'),
                reserved_to=reserved_to.strftime('%Y-%m-%d %H:%M:%S'),
                booking_fee=booking_fee,
            )
        except SQLAlchemyError as err:
            return self._db_error_response(err)

        return jsonify({
            'message': 'M:M reservation created via stored procedure sp_create_reservation_by_values',
            'data': created,
        }), 201

    def insert_noname_batch(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        start_num = data.get('start_num') if isinstance(data, dict) else None
        if start_num is not None:
            try:
                start_num = int(start_num)
            except (ValueError, TypeError) as err:
                return jsonify({'error': f'Invalid start_num: {err}'}), 400

        try:
            rows = self._service.insert_noname_spot_types(start_num=start_num)
        except SQLAlchemyError as err:
            return self._db_error_response(err)

        return jsonify({
            'message': 'Inserted 10 rows via stored procedure sp_insert_noname_spot_types',
            'inserted_count': len(rows),
            'items': rows,
        }), 201

    def get_station_rate_stats(self) -> Tuple[Any, int]:
        stat_type = (request.args.get('stat') or 'ALL').upper()
        if stat_type not in {'ALL', 'MIN', 'MAX', 'AVG', 'SUM'}:
            return jsonify({'error': "Invalid stat parameter. Allowed: ALL, MIN, MAX, AVG, SUM"}), 400

        try:
            stats = self._service.get_parking_station_rate_stats(stat_type=stat_type)
        except SQLAlchemyError as err:
            return self._db_error_response(err)

        return jsonify({
            'procedure': 'sp_get_parking_station_rate_stats',
            'user_defined_function': 'fn_parking_station_rate_stat',
            'stats': stats,
        }), 200

    def split_clients_cursor(self) -> Tuple[Any, int]:
        try:
            result = self._service.split_clients_cursor()
        except SQLAlchemyError as err:
            return self._db_error_response(err)

        return jsonify({
            'message': 'Clients split into two timestamped tables via cursor procedure sp_split_clients_cursor',
            'result': result,
        }), 201

    def get_delete_logs(self) -> Tuple[Any, int]:
        logs = self._service.get_reservation_delete_logs()
        return jsonify({
            'total_logs': len(logs),
            'logs': [log.put_into_dto() for log in logs],
        }), 200
