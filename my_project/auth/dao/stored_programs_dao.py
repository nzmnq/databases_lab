from datetime import datetime, date
from decimal import Decimal
import re
from typing import Any, Dict, List, Optional
from sqlalchemy import text
from my_project import db
from my_project.auth.domain.station_maintenance import ReservationDeleteLog


def _serialize_value(val: Any) -> Any:
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (datetime, date)):
        return val.strftime('%Y-%m-%d %H:%M:%S') if isinstance(val, datetime) else val.isoformat()
    return val


def _serialize_row(row: Any) -> Dict[str, Any]:
    return {key: _serialize_value(value) for key, value in dict(row).items()}


def execute_stored_procedure(sql: str, params: Optional[Dict[str, Any]] = None, commit: bool = False) -> List[Dict[str, Any]]:
    result = db.session.execute(text(sql), params or {})
    try:
        rows = [_serialize_row(row) for row in result.mappings().all()]
    finally:
        result.close()

    if commit:
        db.session.commit()
    return rows


class StoredProgramsDAO:
    def call_insert_station_maintenance(
        self,
        station_id: int,
        inspector_code: str,
        description: str,
        maintenance_cost: float,
    ) -> Optional[Dict[str, Any]]:
        rows = execute_stored_procedure(
            "CALL sp_insert_station_maintenance(:station_id, :inspector_code, :description, :maintenance_cost)",
            {
                'station_id': station_id,
                'inspector_code': inspector_code,
                'description': description,
                'maintenance_cost': maintenance_cost,
            },
            commit=True,
        )
        return rows[0] if rows else None

    def call_create_reservation_by_values(
        self,
        client_email: str,
        spot_number: str,
        license_plate: str,
        reserved_from: str,
        reserved_to: str,
        booking_fee: float,
    ) -> Optional[Dict[str, Any]]:
        rows = execute_stored_procedure(
            "CALL sp_create_reservation_by_values(:client_email, :spot_number, :license_plate, :reserved_from, :reserved_to, :booking_fee)",
            {
                'client_email': client_email,
                'spot_number': spot_number,
                'license_plate': license_plate,
                'reserved_from': reserved_from,
                'reserved_to': reserved_to,
                'booking_fee': booking_fee,
            },
            commit=True,
        )
        return rows[0] if rows else None

    def call_insert_noname_spot_types(self, start_num: Optional[int] = None) -> List[Dict[str, Any]]:
        return execute_stored_procedure(
            "CALL sp_insert_noname_spot_types(:start_num)",
            {'start_num': start_num},
            commit=True,
        )

    def call_get_parking_station_rate_stats(self, stat_type: str = 'ALL') -> Optional[Dict[str, Any]]:
        rows = execute_stored_procedure(
            "CALL sp_get_parking_station_rate_stats(:stat_type)",
            {'stat_type': stat_type},
            commit=False,
        )
        return rows[0] if rows else None

    def call_split_clients_cursor(self) -> Dict[str, Any]:
        rows = execute_stored_procedure("CALL sp_split_clients_cursor()", commit=True)
        summary = rows[0] if rows else {}
        t1 = summary.get('table_1_name')
        t2 = summary.get('table_2_name')
        valid_name = re.compile(r'^clients_copy[12]_[0-9_]+$')

        table_1_data: List[Dict[str, Any]] = []
        table_2_data: List[Dict[str, Any]] = []

        if t1 and valid_name.match(t1):
            res1 = db.session.execute(text(f"SELECT id, client_type, phone, email, registration_date FROM `{t1}` ORDER BY id"))
            table_1_data = [_serialize_row(r) for r in res1.mappings().all()]
            res1.close()

        if t2 and valid_name.match(t2):
            res2 = db.session.execute(text(f"SELECT id, client_type, phone, email, registration_date FROM `{t2}` ORDER BY id"))
            table_2_data = [_serialize_row(r) for r in res2.mappings().all()]
            res2.close()

        return {
            **summary,
            'table_1_data': table_1_data,
            'table_2_data': table_2_data,
        }

    def get_reservation_delete_logs(self) -> List[ReservationDeleteLog]:
        return ReservationDeleteLog.query.order_by(ReservationDeleteLog.id.desc()).all()
