from my_project.auth.dao.parking_ticket_dao import ParkingTicketDAO
from my_project.auth.service.general_service import GeneralService


class ParkingTicketService(GeneralService):
    _dao = ParkingTicketDAO()
