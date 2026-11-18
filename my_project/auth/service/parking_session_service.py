from my_project.auth.dao.parking_session_dao import ParkingSessionDAO
from my_project.auth.service.general_service import GeneralService


class ParkingSessionService(GeneralService):
    _dao = ParkingSessionDAO()
