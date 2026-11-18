from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.station_maintenance import ReservationDeleteLog


class ReservationDeleteLogDAO(GeneralDAO):
    _model = ReservationDeleteLog
