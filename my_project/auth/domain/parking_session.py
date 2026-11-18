from datetime import datetime
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ParkingSession(db.Model, IDTO):
    __tablename__ = 'parking_sessions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(
        db.Integer,
        db.ForeignKey('parking_spots.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    card_id = db.Column(
        db.Integer,
        db.ForeignKey('regular_cards.id', ondelete='SET NULL', onupdate='CASCADE'),
        nullable=True,
    )
    license_plate = db.Column(db.String(16), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)
    status = db.Column(db.Enum('ACTIVE', 'COMPLETED', 'OVERDUE'), nullable=False, default='ACTIVE')

    def put_into_dto(self) -> Dict[str, Any]:
        duration_minutes = (
            int((self.exit_time - self.entry_time).total_seconds() // 60)
            if self.entry_time and self.exit_time
            else None
        )
        return {
            'id': self.id,
            'spot_id': self.spot_id,
            'card_id': self.card_id,
            'license_plate': self.license_plate,
            'entry_time': self.entry_time.strftime('%Y-%m-%d %H:%M:%S') if self.entry_time else None,
            'exit_time': self.exit_time.strftime('%Y-%m-%d %H:%M:%S') if self.exit_time else None,
            'duration_minutes': duration_minutes,
            'total_cost': float(self.total_cost) if self.total_cost is not None else 0.0,
            'status': self.status,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ParkingSession':
        entry_time = dto_dict.get('entry_time')
        exit_time = dto_dict.get('exit_time')
        if isinstance(entry_time, str):
            entry_time = datetime.fromisoformat(entry_time)
        if isinstance(exit_time, str):
            exit_time = datetime.fromisoformat(exit_time)
        return cls(
            spot_id=dto_dict.get('spot_id'),
            card_id=dto_dict.get('card_id'),
            license_plate=dto_dict.get('license_plate'),
            entry_time=entry_time or datetime.utcnow(),
            exit_time=exit_time,
            total_cost=dto_dict.get('total_cost', 0.00),
            status=dto_dict.get('status', 'ACTIVE'),
        )
