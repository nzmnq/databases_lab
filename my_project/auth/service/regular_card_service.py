from my_project.auth.dao.regular_card_dao import RegularCardDAO
from my_project.auth.service.general_service import GeneralService


class RegularCardService(GeneralService):
    _dao = RegularCardDAO()
