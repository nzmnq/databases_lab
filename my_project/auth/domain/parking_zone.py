from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ParkingZone(db.Model, IDTO):
    __tablename__ = 'parking_zones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(
        db.Integer,
        db.ForeignKey('parking_stations.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    floor_level = db.Column(db.Integer, nullable=False, default=0)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'station_id': self.station_id,
            'code': self.code,
            'name': self.name,
            'floor_level': self.floor_level,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ParkingZone':
        return cls(
            station_id=dto_dict.get('station_id'),
            code=dto_dict.get('code'),
            name=dto_dict.get('name'),
            floor_level=dto_dict.get('floor_level', 0),
        )
