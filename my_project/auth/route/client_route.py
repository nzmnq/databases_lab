from flask import Blueprint
from my_project.auth.controller.client_controller import ClientController
from my_project.auth.route.crud_helper import register_crud_routes

clients_bp = Blueprint('clients', __name__, url_prefix='/api/clients')
controller = ClientController()
register_crud_routes(clients_bp, controller)
