from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ParkingSpot(db.Model, IDTO):
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zone_id = db.Column(db.Integer, nullable=False)
    spot_type_id = db.Column(db.Integer, nullable=False)
    spot_number = db.Column(db.String(20), nullable=False)
    current_status = db.Column(
        db.Enum('FREE', 'OCCUPIED', 'RESERVED', 'MAINTENANCE'),
        nullable=False,
        default='FREE',
    )

    reservations = db.relationship('ParkingReservation', back_populates='spot', cascade='all, delete-orphan', lazy=True)
    reserving_clients = db.relationship(
        'Client',
        secondary='parking_reservations',
        back_populates='reserved_spots',
        viewonly=True,
    )

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'zone_id': self.zone_id,
            'spot_type_id': self.spot_type_id,
            'spot_number': self.spot_number,
            'current_status': self.current_status,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ParkingSpot':
        return cls(
            zone_id=dto_dict.get('zone_id'),
            spot_type_id=dto_dict.get('spot_type_id'),
            spot_number=dto_dict.get('spot_number'),
            current_status=dto_dict.get('current_status', 'FREE'),
        )
