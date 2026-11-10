from flask import Blueprint, request
from my_project.auth.controller.retail_chain_controller import RetailChainController

retail_chains_bp = Blueprint('retail_chains', __name__, url_prefix='/api/retail-chains')
controller = RetailChainController()

@retail_chains_bp.route('', methods=['GET'])
@retail_chains_bp.route('/', methods=['GET'])
def get_all_retail_chains():
    return controller.find_all()

@retail_chains_bp.route('/<int:chain_id>', methods=['GET'])
def get_retail_chain_by_id(chain_id: int):
    return controller.find_by_id(chain_id)

@retail_chains_bp.route('', methods=['POST'])
@retail_chains_bp.route('/', methods=['POST'])
def create_retail_chain():
    data = request.get_json(silent=True) or {}
    return controller.create(data)

@retail_chains_bp.route('/<int:chain_id>', methods=['PUT', 'PATCH'])
def update_retail_chain(chain_id: int):
    data = request.get_json(silent=True) or {}
    return controller.update(chain_id, data)

@retail_chains_bp.route('/<int:chain_id>', methods=['DELETE'])
def delete_retail_chain(chain_id: int):
    return controller.delete(chain_id)

@retail_chains_bp.route('/<int:chain_id>/parking-stations', methods=['GET'])
def get_chain_parking_stations(chain_id: int):
    return controller.find_parking_stations(chain_id)
