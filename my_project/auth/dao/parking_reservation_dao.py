from typing import List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.client import Client
from my_project.auth.domain.parking_spot import ParkingSpot
from my_project.auth.domain.parking_reservation import ParkingReservation


class ParkingReservationDAO(GeneralDAO):
    _model = ParkingReservation

    def find_client_by_id(self, client_id: int) -> Optional[Client]:
        return Client.query.get(client_id)

    def find_spot_by_id(self, spot_id: int) -> Optional[ParkingSpot]:
        return ParkingSpot.query.get(spot_id)

    def find_all_clients(self) -> List[Client]:
        return Client.query.all()

    def find_by_client_id(self, client_id: int) -> List[ParkingReservation]:
        return ParkingReservation.query.filter_by(client_id=client_id).all()

    def find_by_spot_id(self, spot_id: int) -> List[ParkingReservation]:
        return ParkingReservation.query.filter_by(spot_id=spot_id).all()
