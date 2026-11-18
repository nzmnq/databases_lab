from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.parking_ticket import ParkingTicket


class ParkingTicketDAO(GeneralDAO):
    _model = ParkingTicket
