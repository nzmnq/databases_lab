from typing import List
from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.parking_station_dao import ParkingStationDAO
from my_project.auth.domain.parking_station import ParkingStation

class ParkingStationService(GeneralService):
    def __init__(self):
        self._dao = ParkingStationDAO()

    def get_by_city(self, city: str) -> List[ParkingStation]:
        return self._dao.find_by_city(city)

    def get_by_chain_id(self, chain_id: int) -> List[ParkingStation]:
        return self._dao.find_by_chain_id(chain_id)
