from flask import Blueprint
from my_project.auth.controller.regular_card_controller import RegularCardController
from my_project.auth.route.crud_helper import register_crud_routes

regular_cards_bp = Blueprint('regular_cards', __name__, url_prefix='/api/regular-cards')
controller = RegularCardController()
register_crud_routes(regular_cards_bp, controller)
