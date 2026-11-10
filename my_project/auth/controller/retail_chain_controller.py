from typing import Tuple, Any, Dict
from flask import jsonify
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.retail_chain_service import RetailChainService
from my_project.auth.domain.retail_chain import RetailChain

class RetailChainController(GeneralController):
    def __init__(self):
        self._service = RetailChainService()

    def create(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        name = data.get('name')
        edrpou = data.get('edrpou')
        support_phone = data.get('support_phone')

        if not name or not edrpou or not support_phone:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['name', 'edrpou', 'support_phone']
            }), 400

        # Uniqueness checks
        if self._service.get_by_name(name):
            return jsonify({'error': f"Retail chain with name '{name}' already exists"}), 409
        if self._service.get_by_edrpou(edrpou):
            return jsonify({'error': f"Retail chain with EDRPOU '{edrpou}' already exists"}), 409

        entity = RetailChain.create_from_dto(data)
        created_entity = self._service.create(entity)
        return jsonify(created_entity.put_into_dto()), 201

    def update(self, entity_id: int, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        existing = self._service.get_by_id(entity_id)
        if not existing:
            return jsonify({'error': 'Retail chain not found', 'id': entity_id}), 404

        # Validate unique conflicts if updating name or edrpou
        if 'name' in data and data['name'] != existing.name:
            if self._service.get_by_name(data['name']):
                return jsonify({'error': f"Retail chain with name '{data['name']}' already exists"}), 409

        if 'edrpou' in data and data['edrpou'] != existing.edrpou:
            if self._service.get_by_edrpou(data['edrpou']):
                return jsonify({'error': f"Retail chain with EDRPOU '{data['edrpou']}' already exists"}), 409

        updated = self._service.update(entity_id, data)
        return jsonify(updated.put_into_dto()), 200

    def find_parking_stations(self, chain_id: int) -> Tuple[Any, int]:
        """
        Returns all parking stations associated with a specific retail chain (1:M / M:1 relation).
        """
        chain = self._service.get_by_id(chain_id)
        if not chain:
            return jsonify({'error': 'Retail chain not found', 'id': chain_id}), 404

        stations = self._service.get_parking_stations(chain_id)
        dtos = [station.put_into_dto() for station in stations]
        return jsonify({
            'retail_chain_id': chain.id,
            'retail_chain_name': chain.name,
            'total_stations': len(dtos),
            'parking_stations': dtos
        }), 200
