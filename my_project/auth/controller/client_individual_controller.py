from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.client_individual_service import ClientIndividualService


class ClientIndividualController(GeneralController):
    _service = ClientIndividualService()
    _required_fields = ['client_id', 'first_name', 'last_name', 'tax_id', 'driver_license']
