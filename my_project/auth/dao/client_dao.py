from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.client import Client


class ClientDAO(GeneralDAO):
    _model = Client
