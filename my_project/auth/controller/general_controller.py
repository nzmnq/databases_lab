from abc import ABC
from typing import Tuple, Any
from flask import jsonify

class GeneralController(ABC):
    _service: Any = None

    def find_all(self) -> Tuple[Any, int]:
        entities = self._service.get_all()
        dtos = [entity.put_into_dto() for entity in entities]
        return jsonify(dtos), 200

    def find_by_id(self, entity_id: int) -> Tuple[Any, int]:
        entity = self._service.get_by_id(entity_id)
        if not entity:
            return jsonify({'error': 'Resource not found', 'id': entity_id}), 404
        return jsonify(entity.put_into_dto()), 200

    def delete(self, entity_id: int) -> Tuple[Any, int]:
        success = self._service.delete(entity_id)
        if not success:
            return jsonify({'error': 'Resource not found or could not be deleted', 'id': entity_id}), 404
        return jsonify({'message': 'Resource deleted successfully', 'id': entity_id}), 200
