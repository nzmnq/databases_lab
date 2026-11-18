from typing import Any, Dict, List, Optional
from my_project.auth.dao.station_maintenance_dao import StationMaintenanceDAO
from my_project.auth.domain.station_maintenance import StationMaintenance
from my_project.auth.service.general_service import GeneralService


class StationMaintenanceService(GeneralService):
    _dao = StationMaintenanceDAO()

    def get_by_station_id(self, station_id: int) -> List[StationMaintenance]:
        return self._dao.find_by_station_id(station_id)

    def create_via_procedure(
        self,
        station_id: int,
        inspector_code: str,
        description: str,
        maintenance_cost: float,
    ) -> Optional[Dict[str, Any]]:
        return self._dao.insert_via_procedure(
            station_id=station_id,
            inspector_code=inspector_code,
            description=description,
            maintenance_cost=maintenance_cost,
        )
