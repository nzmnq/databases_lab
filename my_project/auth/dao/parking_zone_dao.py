from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.parking_zone import ParkingZone


class ParkingZoneDAO(GeneralDAO):
    _model = ParkingZone
