from abc import ABC
from typing import List, Optional, Any, Dict

class GeneralService(ABC):
    _dao: Any = None

    def get_all(self) -> List[Any]:
        return self._dao.find_all()

    def get_by_id(self, entity_id: int) -> Optional[Any]:
        return self._dao.find_by_id(entity_id)

    def create(self, entity: Any) -> Any:
        return self._dao.create(entity)

    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[Any]:
        return self._dao.update(entity_id, data)

    def delete(self, entity_id: int) -> bool:
        return self._dao.delete(entity_id)
