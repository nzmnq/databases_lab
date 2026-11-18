from typing import Any
from flask import Blueprint, request


def register_crud_routes(bp: Blueprint, controller: Any) -> None:
    @bp.route('', methods=['GET'])
    @bp.route('/', methods=['GET'])
    def get_all():
        return controller.find_all()

    @bp.route('/<int:entity_id>', methods=['GET'])
    def get_by_id(entity_id: int):
        return controller.find_by_id(entity_id)

    @bp.route('', methods=['POST'])
    @bp.route('/', methods=['POST'])
    def create_item():
        data = request.get_json(silent=True) or {}
        return controller.create(data)

    @bp.route('/<int:entity_id>', methods=['PUT', 'PATCH'])
    def update_item(entity_id: int):
        data = request.get_json(silent=True) or {}
        return controller.update(entity_id, data)

    @bp.route('/<int:entity_id>', methods=['DELETE'])
    def delete_item(entity_id: int):
        return controller.delete(entity_id)
