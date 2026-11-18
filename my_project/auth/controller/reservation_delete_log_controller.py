from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.reservation_delete_log_service import ReservationDeleteLogService


class ReservationDeleteLogController(GeneralController):
    _service = ReservationDeleteLogService()
    _required_fields = ['reservation_id', 'client_id', 'spot_id', 'license_plate', 'status']
