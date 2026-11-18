from typing import Any, Dict, List, Optional
from my_project.auth.dao.stored_programs_dao import StoredProgramsDAO
from my_project.auth.domain.station_maintenance import ReservationDeleteLog


class StoredProgramsService:
    def __init__(self):
        self._dao = StoredProgramsDAO()

    def insert_station_maintenance(
        self,
        station_id: int,
        inspector_code: str,
        description: str,
        maintenance_cost: float,
    ) -> Optional[Dict[str, Any]]:
        return self._dao.call_insert_station_maintenance(
            station_id=station_id,
            inspector_code=inspector_code,
            description=description,
            maintenance_cost=maintenance_cost,
        )

    def create_reservation_by_values(
        self,
        client_email: str,
        spot_number: str,
        license_plate: str,
        reserved_from: str,
        reserved_to: str,
        booking_fee: float,
    ) -> Optional[Dict[str, Any]]:
        return self._dao.call_create_reservation_by_values(
            client_email=client_email,
            spot_number=spot_number,
            license_plate=license_plate,
            reserved_from=reserved_from,
            reserved_to=reserved_to,
            booking_fee=booking_fee,
        )

    def insert_noname_spot_types(self, start_num: Optional[int] = None) -> List[Dict[str, Any]]:
        return self._dao.call_insert_noname_spot_types(start_num=start_num)

    def get_parking_station_rate_stats(self, stat_type: str = 'ALL') -> Optional[Dict[str, Any]]:
        return self._dao.call_get_parking_station_rate_stats(stat_type=stat_type)

    def split_clients_cursor(self) -> Dict[str, Any]:
        return self._dao.call_split_clients_cursor()

    def get_reservation_delete_logs(self) -> List[ReservationDeleteLog]:
        return self._dao.get_reservation_delete_logs()
