from my_project.auth.dao.spot_type_dao import SpotTypeDAO
from my_project.auth.service.general_service import GeneralService


class SpotTypeService(GeneralService):
    _dao = SpotTypeDAO()
