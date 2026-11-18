from my_project.auth.dao.parking_spot_dao import ParkingSpotDAO
from my_project.auth.service.general_service import GeneralService


class ParkingSpotService(GeneralService):
    _dao = ParkingSpotDAO()
