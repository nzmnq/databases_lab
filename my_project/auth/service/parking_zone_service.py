from my_project.auth.dao.parking_zone_dao import ParkingZoneDAO
from my_project.auth.service.general_service import GeneralService


class ParkingZoneService(GeneralService):
    _dao = ParkingZoneDAO()
