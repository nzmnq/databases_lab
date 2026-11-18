from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class Vehicle(db.Model, IDTO):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=True,
    )
    license_plate = db.Column(db.String(16), nullable=False, unique=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=True)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'client_id': self.client_id,
            'license_plate': self.license_plate,
            'make': self.make,
            'model': self.model,
            'color': self.color,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'Vehicle':
        return cls(
            client_id=dto_dict.get('client_id'),
            license_plate=dto_dict.get('license_plate'),
            make=dto_dict.get('make'),
            model=dto_dict.get('model'),
            color=dto_dict.get('color'),
        )
