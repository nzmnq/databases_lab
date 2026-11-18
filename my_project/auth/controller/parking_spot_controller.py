from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.parking_spot_service import ParkingSpotService


class ParkingSpotController(GeneralController):
    _service = ParkingSpotService()
    _required_fields = ['zone_id', 'spot_type_id', 'spot_number']
