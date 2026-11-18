from my_project.auth.dao.vehicle_dao import VehicleDAO
from my_project.auth.service.general_service import GeneralService


class VehicleService(GeneralService):
    _dao = VehicleDAO()
