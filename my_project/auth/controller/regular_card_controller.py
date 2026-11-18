from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.regular_card_service import RegularCardService


class RegularCardController(GeneralController):
    _service = RegularCardService()
    _required_fields = ['client_id', 'card_number', 'card_type', 'issue_date', 'expiry_date']
