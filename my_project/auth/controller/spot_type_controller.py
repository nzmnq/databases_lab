from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.spot_type_service import SpotTypeService


class SpotTypeController(GeneralController):
    _service = SpotTypeService()
    _required_fields = ['type_name']
