from flask import Blueprint
from my_project.auth.controller.client_individual_controller import ClientIndividualController
from my_project.auth.route.crud_helper import register_crud_routes

client_individuals_bp = Blueprint('client_individuals', __name__, url_prefix='/api/client-individuals')
controller = ClientIndividualController()
register_crud_routes(client_individuals_bp, controller)
