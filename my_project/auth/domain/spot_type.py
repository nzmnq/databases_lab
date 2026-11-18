from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class SpotType(db.Model, IDTO):
    __tablename__ = 'spot_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    tariff_multiplier = db.Column(db.Numeric(4, 2), nullable=False, default=1.00)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type_name': self.type_name,
            'description': self.description,
            'tariff_multiplier': float(self.tariff_multiplier) if self.tariff_multiplier is not None else 1.0,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'SpotType':
        return cls(
            type_name=dto_dict.get('type_name'),
            description=dto_dict.get('description'),
            tariff_multiplier=dto_dict.get('tariff_multiplier', 1.00),
        )
