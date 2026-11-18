from my_project.auth.dao.client_dao import ClientDAO
from my_project.auth.service.general_service import GeneralService


class ClientService(GeneralService):
    _dao = ClientDAO()
