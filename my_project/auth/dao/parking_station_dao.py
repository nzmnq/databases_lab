from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.parking_station import ParkingStation

class ParkingStationDAO(GeneralDAO):
    _model = ParkingStation

    def find_by_city(self, city: str) -> List[ParkingStation]:
        return self._model.query.filter_by(city=city).all()

    def find_by_chain_id(self, chain_id: int) -> List[ParkingStation]:
        return self._model.query.filter_by(chain_id=chain_id).all()
