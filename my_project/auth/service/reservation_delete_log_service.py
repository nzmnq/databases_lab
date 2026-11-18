from my_project.auth.dao.reservation_delete_log_dao import ReservationDeleteLogDAO
from my_project.auth.service.general_service import GeneralService


class ReservationDeleteLogService(GeneralService):
    _dao = ReservationDeleteLogDAO()
