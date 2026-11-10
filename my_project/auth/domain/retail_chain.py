from datetime import datetime
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO

class RetailChain(db.Model, IDTO):
    __tablename__ = 'retail_chains'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    edrpou = db.Column(db.String(10), nullable=False, unique=True)
    website = db.Column(db.String(150), nullable=True)
    support_phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    parking_stations = db.relationship(
        'ParkingStation',
        back_populates='retail_chain',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __repr__(self):
        return f"<RetailChain id={self.id} name='{self.name}' edrpou='{self.edrpou}'>"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'edrpou': self.edrpou,
            'website': self.website,
            'support_phone': self.support_phone,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'parking_stations_count': len(self.parking_stations) if self.parking_stations is not None else 0
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'RetailChain':
        return cls(
            name=dto_dict.get('name'),
            edrpou=dto_dict.get('edrpou'),
            website=dto_dict.get('website'),
            support_phone=dto_dict.get('support_phone')
        )
