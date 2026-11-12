from datetime import datetime
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ParkingReservation(db.Model, IDTO):
    """Junction table implementing M:M between clients and parking_spots."""

    __tablename__ = 'parking_reservations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    license_plate = db.Column(db.String(16), nullable=False)
    reserved_from = db.Column(db.DateTime, nullable=False)
    reserved_to = db.Column(db.DateTime, nullable=False)
    booking_fee = db.Column(db.Numeric(8, 2), nullable=False, default=0.00)
    status = db.Column(
        db.Enum('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', 'NO_SHOW'),
        nullable=False,
        default='CONFIRMED',
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    client = db.relationship('Client', back_populates='reservations')
    spot = db.relationship('ParkingSpot', back_populates='reservations')

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_phone': self.client.phone if self.client else None,
            'client_email': self.client.email if self.client else None,
            'spot_id': self.spot_id,
            'spot_number': self.spot.spot_number if self.spot else None,
            'license_plate': self.license_plate,
            'reserved_from': self.reserved_from.strftime('%Y-%m-%d %H:%M:%S') if self.reserved_from else None,
            'reserved_to': self.reserved_to.strftime('%Y-%m-%d %H:%M:%S') if self.reserved_to else None,
            'booking_fee': float(self.booking_fee) if self.booking_fee is not None else 0.0,
            'status': self.status,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ParkingReservation':
        reserved_from = dto_dict.get('reserved_from')
        reserved_to = dto_dict.get('reserved_to')
        if isinstance(reserved_from, str):
            reserved_from = datetime.fromisoformat(reserved_from)
        if isinstance(reserved_to, str):
            reserved_to = datetime.fromisoformat(reserved_to)
        return cls(
            spot_id=dto_dict.get('spot_id'),
            client_id=dto_dict.get('client_id'),
            license_plate=dto_dict.get('license_plate'),
            reserved_from=reserved_from,
            reserved_to=reserved_to,
            booking_fee=dto_dict.get('booking_fee', 0.00),
            status=dto_dict.get('status', 'CONFIRMED'),
        )
