from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.parking_spot import ParkingSpot


class ParkingSpotDAO(GeneralDAO):
    _model = ParkingSpot
