from typing import Tuple, Any, Dict
from flask import jsonify
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.parking_station_service import ParkingStationService
from my_project.auth.service.retail_chain_service import RetailChainService
from my_project.auth.domain.parking_station import ParkingStation

class ParkingStationController(GeneralController):
    def __init__(self):
        self._service = ParkingStationService()
        self._chain_service = RetailChainService()

    def create(self, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        chain_id = data.get('chain_id')
        name = data.get('name')
        city = data.get('city')
        address = data.get('address')

        if not chain_id or not name or not city or not address:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['chain_id', 'name', 'city', 'address']
            }), 400

        # Foreign key validation
        parent_chain = self._chain_service.get_by_id(chain_id)
        if not parent_chain:
            return jsonify({'error': f"Parent retail chain with id {chain_id} does not exist"}), 400

        entity = ParkingStation.create_from_dto(data)
        created_entity = self._service.create(entity)
        return jsonify(created_entity.put_into_dto()), 201

    def update(self, entity_id: int, data: Dict[str, Any]) -> Tuple[Any, int]:
        if not data:
            return jsonify({'error': 'Request body must be a valid JSON object'}), 400

        existing = self._service.get_by_id(entity_id)
        if not existing:
            return jsonify({'error': 'Parking station not found', 'id': entity_id}), 404

        if 'chain_id' in data:
            parent_chain = self._chain_service.get_by_id(data['chain_id'])
            if not parent_chain:
                return jsonify({'error': f"Parent retail chain with id {data['chain_id']} does not exist"}), 400

        updated = self._service.update(entity_id, data)
        return jsonify(updated.put_into_dto()), 200

    def find_parent_chain(self, station_id: int) -> Tuple[Any, int]:
        """
        Returns parent retail chain for given parking station (M:1 relationship).
        """
        station = self._service.get_by_id(station_id)
        if not station:
            return jsonify({'error': 'Parking station not found', 'id': station_id}), 404

        if not station.retail_chain:
            return jsonify({'error': 'No associated retail chain found'}), 404

        return jsonify({
            'parking_station_id': station.id,
            'parking_station_name': station.name,
            'retail_chain': station.retail_chain.put_into_dto()
        }), 200
