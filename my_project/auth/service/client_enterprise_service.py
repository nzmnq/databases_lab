from my_project.auth.dao.client_enterprise_dao import ClientEnterpriseDAO
from my_project.auth.service.general_service import GeneralService


class ClientEnterpriseService(GeneralService):
    _dao = ClientEnterpriseDAO()
