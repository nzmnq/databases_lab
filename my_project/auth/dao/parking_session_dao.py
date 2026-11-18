from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.parking_session import ParkingSession


class ParkingSessionDAO(GeneralDAO):
    _model = ParkingSession
