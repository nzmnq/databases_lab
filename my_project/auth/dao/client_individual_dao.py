from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.client_individual import ClientIndividual


class ClientIndividualDAO(GeneralDAO):
    _model = ClientIndividual
