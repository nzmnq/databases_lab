from my_project.auth.dao.client_individual_dao import ClientIndividualDAO
from my_project.auth.service.general_service import GeneralService


class ClientIndividualService(GeneralService):
    _dao = ClientIndividualDAO()
