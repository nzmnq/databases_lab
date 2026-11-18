from abc import ABC
from typing import Tuple, Any, Dict, List
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from my_project import db


def extract_db_error_message(err: SQLAlchemyError) -> str:
    orig = getattr(err, 'orig', None)
    if orig is not None:
        args = getattr(orig, 'args', None)
        if args and len(args) >= 2:
            return str(args[1])
        return str(orig)
    return str(err)


class GeneralController(ABC):
    _service: Any = None
    _required_fields: List[str] = []

    def find_all(self) -> Tuple[Any, int]:
        entities = self._service.get_all()
        dtos = [entity.put_into_dto() for entity in entities]
        return jsonify(dtos), 200

    def find_by_id(self, entity_id: int) -> Tuple[Any, int]:
        entity = self._service.get_by_id(entity_id)
        if not entity:
            return jsonify({'error': 'Resource not found', 'id': entity_id}), 404
        return jsonify(entity.put_into_dto()), 200

    def create(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        missing = [f for f in self._required_fields if data.get(f) is None or data.get(f) == '']
        if missing:
            return jsonify({
                'error': 'Missing required fields',
                'required': self._required_fields,
                'missing': missing,
            }), 400

        try:
            entity = self._service._dao._model.create_from_dto(data)
            created = self._service.create(entity)
        except (ValueError, TypeError) as err:
            db.session.rollback()
            return jsonify({'error': f'Invalid parameter format: {err}'}), 400
        except SQLAlchemyError as err:
            db.session.rollback()
            return jsonify({
                'error': 'Database Trigger / Integrity Error',
                'details': extract_db_error_message(err),
            }), 400

        return jsonify(created.put_into_dto()), 201

    def update(self, entity_id: int, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        existing = self._service.get_by_id(entity_id)
        if not existing:
            return jsonify({'error': 'Resource not found', 'id': entity_id}), 404

        try:
            updated = self._service.update(entity_id, data)
        except (ValueError, TypeError) as err:
            db.session.rollback()
            return jsonify({'error': f'Invalid parameter format: {err}'}), 400
        except SQLAlchemyError as err:
            db.session.rollback()
            return jsonify({
                'error': 'Database Trigger / Integrity Error',
                'details': extract_db_error_message(err),
            }), 400

        return jsonify(updated.put_into_dto()), 200

    def delete(self, entity_id: int) -> Tuple[Any, int]:
        try:
            success = self._service.delete(entity_id)
        except SQLAlchemyError as err:
            db.session.rollback()
            return jsonify({
                'error': 'Database Trigger / Integrity Error',
                'details': extract_db_error_message(err),
            }), 400
        if not success:
            return jsonify({'error': 'Resource not found or could not be deleted', 'id': entity_id}), 404
        return jsonify({'message': 'Resource deleted successfully', 'id': entity_id}), 200
