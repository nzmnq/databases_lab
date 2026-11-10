from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO

class ParkingStation(db.Model, IDTO):
    __tablename__ = 'parking_stations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('retail_chains.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=True)
    longitude = db.Column(db.Numeric(11, 8), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    hourly_rate = db.Column(db.Numeric(8, 2), nullable=False, default=30.00)
    is_24_7 = db.Column(db.Boolean, nullable=False, default=True)

    retail_chain = db.relationship('RetailChain', back_populates='parking_stations')

    def __repr__(self):
        return f"<ParkingStation id={self.id} name='{self.name}' city='{self.city}' chain_id={self.chain_id}>"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'chain_id': self.chain_id,
            'chain_name': self.retail_chain.name if self.retail_chain else None,
            'name': self.name,
            'city': self.city,
            'address': self.address,
            'latitude': float(self.latitude) if self.latitude is not None else None,
            'longitude': float(self.longitude) if self.longitude is not None else None,
            'capacity': self.capacity,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate is not None else None,
            'is_24_7': bool(self.is_24_7)
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ParkingStation':
        return cls(
            chain_id=dto_dict.get('chain_id'),
            name=dto_dict.get('name'),
            city=dto_dict.get('city'),
            address=dto_dict.get('address'),
            latitude=dto_dict.get('latitude'),
            longitude=dto_dict.get('longitude'),
            capacity=dto_dict.get('capacity', 0),
            hourly_rate=dto_dict.get('hourly_rate', 30.00),
            is_24_7=dto_dict.get('is_24_7', True)
        )
