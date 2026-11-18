from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.parking_ticket_service import ParkingTicketService


class ParkingTicketController(GeneralController):
    _service = ParkingTicketService()
    _required_fields = ['session_id', 'ticket_number']
