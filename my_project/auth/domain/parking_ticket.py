from datetime import datetime
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDTO


class ParkingTicket(db.Model, IDTO):
    __tablename__ = 'parking_tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('parking_sessions.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        unique=True,
    )
    ticket_number = db.Column(db.String(32), nullable=False, unique=True)
    issue_time = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.Enum('UNPAID', 'PAID', 'EXEMPT'), nullable=False, default='UNPAID')
    paid_time = db.Column(db.DateTime, nullable=True)
    paid_amount = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)
    payment_method = db.Column(db.Enum('CASH', 'CARD', 'MOBILE_APP', 'SUBSCRIPTION'), nullable=True)

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'session_id': self.session_id,
            'ticket_number': self.ticket_number,
            'issue_time': self.issue_time.strftime('%Y-%m-%d %H:%M:%S') if self.issue_time else None,
            'payment_status': self.payment_status,
            'paid_time': self.paid_time.strftime('%Y-%m-%d %H:%M:%S') if self.paid_time else None,
            'paid_amount': float(self.paid_amount) if self.paid_amount is not None else 0.0,
            'payment_method': self.payment_method,
        }

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]) -> 'ParkingTicket':
        issue_time = dto_dict.get('issue_time')
        paid_time = dto_dict.get('paid_time')
        if isinstance(issue_time, str):
            issue_time = datetime.fromisoformat(issue_time)
        if isinstance(paid_time, str):
            paid_time = datetime.fromisoformat(paid_time)
        return cls(
            session_id=dto_dict.get('session_id'),
            ticket_number=dto_dict.get('ticket_number'),
            issue_time=issue_time or datetime.utcnow(),
            payment_status=dto_dict.get('payment_status', 'UNPAID'),
            paid_time=paid_time,
            paid_amount=dto_dict.get('paid_amount', 0.00),
            payment_method=dto_dict.get('payment_method'),
        )
