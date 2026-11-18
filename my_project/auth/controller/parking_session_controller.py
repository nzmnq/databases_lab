from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.parking_session_service import ParkingSessionService


class ParkingSessionController(GeneralController):
    _service = ParkingSessionService()
    _required_fields = ['spot_id', 'license_plate']
