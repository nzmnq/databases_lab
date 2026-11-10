from typing import List, Optional
from my_project.auth.service.general_service import GeneralService
from my_project.auth.dao.retail_chain_dao import RetailChainDAO
from my_project.auth.domain.retail_chain import RetailChain
from my_project.auth.domain.parking_station import ParkingStation

class RetailChainService(GeneralService):
    def __init__(self):
        self._dao = RetailChainDAO()

    def get_by_edrpou(self, edrpou: str) -> Optional[RetailChain]:
        return self._dao.find_by_edrpou(edrpou)

    def get_by_name(self, name: str) -> Optional[RetailChain]:
        return self._dao.find_by_name(name)

    def get_parking_stations(self, chain_id: int) -> Optional[List[ParkingStation]]:
        return self._dao.find_parking_stations_by_chain_id(chain_id)
