from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.client_enterprise import ClientEnterprise


class ClientEnterpriseDAO(GeneralDAO):
    _model = ClientEnterprise
