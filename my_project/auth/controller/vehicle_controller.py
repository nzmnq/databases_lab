from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.vehicle_service import VehicleService


class VehicleController(GeneralController):
    _service = VehicleService()
    _required_fields = ['license_plate', 'make', 'model']
