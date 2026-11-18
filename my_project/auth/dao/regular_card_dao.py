from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.regular_card import RegularCard


class RegularCardDAO(GeneralDAO):
    _model = RegularCard
