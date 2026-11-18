from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.parking_zone_service import ParkingZoneService


class ParkingZoneController(GeneralController):
    _service = ParkingZoneService()
    _required_fields = ['station_id', 'code', 'name']
