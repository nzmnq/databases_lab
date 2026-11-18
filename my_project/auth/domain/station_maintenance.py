from datetime import datetime
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class StationMaintenance(db.Model, IDTO):
    __tablename__ = 'station_maintenances'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.Integer, nullable=False)
    inspector_code = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    maintenance_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    performed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'station_id': self.station_id,
            'inspector_code': self.inspector_code,
            'description': self.description,
            'maintenance_cost': float(self.maintenance_cost) if self.maintenance_cost is not None else 0.0,
            'performed_at': self.performed_at.strftime('%Y-%m-%d %H:%M:%S') if self.performed_at else None,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'StationMaintenance':
        performed_at = dto_dict.get('performed_at')
        if isinstance(performed_at, str):
            performed_at = datetime.fromisoformat(performed_at)
        return cls(
            station_id=dto_dict.get('station_id'),
            inspector_code=dto_dict.get('inspector_code'),
            description=dto_dict.get('description'),
            maintenance_cost=dto_dict.get('maintenance_cost', 0.00),
            performed_at=performed_at or datetime.utcnow(),
        )


class ReservationDeleteLog(db.Model, IDTO):
    __tablename__ = 'reservation_delete_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_id = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    spot_id = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'reservation_id': self.reservation_id,
            'client_id': self.client_id,
            'spot_id': self.spot_id,
            'license_plate': self.license_plate,
            'status': self.status,
            'deleted_at': self.deleted_at.strftime('%Y-%m-%d %H:%M:%S') if self.deleted_at else None,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ReservationDeleteLog':
        return cls(
            reservation_id=dto_dict.get('reservation_id'),
            client_id=dto_dict.get('client_id'),
            spot_id=dto_dict.get('spot_id'),
            license_plate=dto_dict.get('license_plate'),
            status=dto_dict.get('status'),
        )
