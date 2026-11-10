from typing import Optional, List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.retail_chain import RetailChain
from my_project.auth.domain.parking_station import ParkingStation

class RetailChainDAO(GeneralDAO):
    _model = RetailChain

    def find_by_edrpou(self, edrpou: str) -> Optional[RetailChain]:
        return self._model.query.filter_by(edrpou=edrpou).first()

    def find_by_name(self, name: str) -> Optional[RetailChain]:
        return self._model.query.filter_by(name=name).first()

    def find_parking_stations_by_chain_id(self, chain_id: int) -> Optional[List[ParkingStation]]:
        chain = self.find_by_id(chain_id)
        if not chain:
            return None
        return chain.parking_stations
