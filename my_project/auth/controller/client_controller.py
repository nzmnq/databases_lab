from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.client_service import ClientService


class ClientController(GeneralController):
    _service = ClientService()
    _required_fields = ['phone', 'email']
