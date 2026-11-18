from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.spot_type import SpotType


class SpotTypeDAO(GeneralDAO):
    _model = SpotType
