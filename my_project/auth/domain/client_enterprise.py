from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ClientEnterprise(db.Model, IDTO):
    __tablename__ = 'client_enterprises'

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        autoincrement=False,
    )
    company_name = db.Column(db.String(150), nullable=False)
    edrpou_code = db.Column(db.String(10), nullable=False, unique=True)
    contact_person = db.Column(db.String(120), nullable=False)
    legal_address = db.Column(db.String(250), nullable=False)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'client_id': self.client_id,
            'company_name': self.company_name,
            'edrpou_code': self.edrpou_code,
            'contact_person': self.contact_person,
            'legal_address': self.legal_address,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ClientEnterprise':
        return cls(
            client_id=dto_dict.get('client_id'),
            company_name=dto_dict.get('company_name'),
            edrpou_code=dto_dict.get('edrpou_code'),
            contact_person=dto_dict.get('contact_person'),
            legal_address=dto_dict.get('legal_address'),
        )
