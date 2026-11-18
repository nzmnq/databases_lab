from flask import Blueprint
from my_project.auth.controller.client_enterprise_controller import ClientEnterpriseController
from my_project.auth.route.crud_helper import register_crud_routes

client_enterprises_bp = Blueprint('client_enterprises', __name__, url_prefix='/api/client-enterprises')
controller = ClientEnterpriseController()
register_crud_routes(client_enterprises_bp, controller)
