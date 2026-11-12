from typing import Any, Dict, List, Optional
from my_project.auth.dao.parking_reservation_dao import ParkingReservationDAO
from my_project.auth.domain.client import Client
from my_project.auth.domain.parking_reservation import ParkingReservation
from my_project.auth.domain.parking_spot import ParkingSpot
from my_project.auth.service.general_service import GeneralService


class ParkingReservationService(GeneralService):
    _dao = ParkingReservationDAO()

    def get_client(self, client_id: int) -> Optional[Client]:
        return self._dao.find_client_by_id(client_id)

    def get_spot(self, spot_id: int) -> Optional[ParkingSpot]:
        return self._dao.find_spot_by_id(spot_id)

    def get_by_client_id(self, client_id: int) -> List[ParkingReservation]:
        return self._dao.find_by_client_id(client_id)

    def get_by_spot_id(self, spot_id: int) -> List[ParkingReservation]:
        return self._dao.find_by_spot_id(spot_id)

    def get_grouped_by_clients(self) -> List[Dict[str, Any]]:
        clients = self._dao.find_all_clients()
        return [
            {
                **client.put_into_dto(),
                'reserved_spots': [spot.put_into_dto() for spot in client.reserved_spots],
            }
            for client in clients
        ]
