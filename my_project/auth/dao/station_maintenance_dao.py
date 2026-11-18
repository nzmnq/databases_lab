from typing import Any, Dict, List, Optional
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.dao.stored_programs_dao import StoredProgramsDAO
from my_project.auth.domain.station_maintenance import StationMaintenance


class StationMaintenanceDAO(GeneralDAO):
    _model = StationMaintenance
    _stored_programs_dao = StoredProgramsDAO()

    def find_by_station_id(self, station_id: int) -> List[StationMaintenance]:
        return self._model.query.filter_by(station_id=station_id).all()

    def insert_via_procedure(
        self,
        station_id: int,
        inspector_code: str,
        description: str,
        maintenance_cost: float,
    ) -> Optional[Dict[str, Any]]:
        return self._stored_programs_dao.call_insert_station_maintenance(
            station_id=station_id,
            inspector_code=inspector_code,
            description=description,
            maintenance_cost=maintenance_cost,
        )
