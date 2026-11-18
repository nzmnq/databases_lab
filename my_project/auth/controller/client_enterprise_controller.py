from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.service.client_enterprise_service import ClientEnterpriseService


class ClientEnterpriseController(GeneralController):
    _service = ClientEnterpriseService()
    _required_fields = ['client_id', 'company_name', 'edrpou_code', 'contact_person', 'legal_address']
