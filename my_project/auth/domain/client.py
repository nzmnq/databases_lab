from datetime import datetime
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class Client(db.Model, IDTO):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_type = db.Column(db.Enum('INDIVIDUAL', 'ENTERPRISE'), nullable=False, default='INDIVIDUAL')
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reservations = db.relationship('ParkingReservation', back_populates='client', cascade='all, delete-orphan', lazy=True)
    reserved_spots = db.relationship(
        'ParkingSpot',
        secondary='parking_reservations',
        back_populates='reserving_clients',
        viewonly=True,
    )

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'client_type': self.client_type,
            'phone': self.phone,
            'email': self.email,
            'registration_date': self.registration_date.strftime('%Y-%m-%d %H:%M:%S') if self.registration_date else None,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'Client':
        return cls(
            client_type=dto_dict.get('client_type', 'INDIVIDUAL'),
            phone=dto_dict.get('phone'),
            email=dto_dict.get('email'),
        )
