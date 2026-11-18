from datetime import date
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class RegularCard(db.Model, IDTO):
    __tablename__ = 'regular_cards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('clients.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    card_number = db.Column(db.String(32), nullable=False, unique=True)
    card_type = db.Column(db.Enum('PREPAID', 'POSTPAID', 'CORPORATE_VIP'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    discount_percent = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    status = db.Column(db.Enum('ACTIVE', 'BLOCKED', 'EXPIRED'), nullable=False, default='ACTIVE')

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'client_id': self.client_id,
            'card_number': self.card_number,
            'card_type': self.card_type,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'balance': float(self.balance) if self.balance is not None else 0.0,
            'discount_percent': float(self.discount_percent) if self.discount_percent is not None else 0.0,
            'status': self.status,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'RegularCard':
        issue_date = dto_dict.get('issue_date')
        expiry_date = dto_dict.get('expiry_date')
        if isinstance(issue_date, str):
            issue_date = date.fromisoformat(issue_date[:10])
        if isinstance(expiry_date, str):
            expiry_date = date.fromisoformat(expiry_date[:10])
        return cls(
            client_id=dto_dict.get('client_id'),
            card_number=dto_dict.get('card_number'),
            card_type=dto_dict.get('card_type'),
            issue_date=issue_date,
            expiry_date=expiry_date,
            balance=dto_dict.get('balance', 0.00),
            discount_percent=dto_dict.get('discount_percent', 0.00),
            status=dto_dict.get('status', 'ACTIVE'),
        )
