from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.vehicle import Vehicle


class VehicleDAO(GeneralDAO):
    _model = Vehicle
