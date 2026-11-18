from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ClientIndividual(db.Model, IDTO):
    __tablename__ = 'client_individuals'

    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        autoincrement=False,
    )
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    tax_id = db.Column(db.String(12), nullable=False, unique=True)
    driver_license = db.Column(db.String(20), nullable=False, unique=True)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'client_id': self.client_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'tax_id': self.tax_id,
            'driver_license': self.driver_license,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ClientIndividual':
        return cls(
            client_id=dto_dict.get('client_id'),
            first_name=dto_dict.get('first_name'),
            last_name=dto_dict.get('last_name'),
            tax_id=dto_dict.get('tax_id'),
            driver_license=dto_dict.get('driver_license'),
        )
