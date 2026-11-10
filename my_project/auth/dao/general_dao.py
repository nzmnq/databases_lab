from abc import ABC
from typing import List, Optional, Any, Dict
from my_project import db

class GeneralDAO(ABC):
    _model: Any = None

    def find_all(self) -> List[Any]:
        return self._model.query.all()

    def find_by_id(self, entity_id: int) -> Optional[Any]:
        if hasattr(db.session, 'get'):
            return db.session.get(self._model, entity_id)
        return self._model.query.get(entity_id)

    def create(self, entity: Any) -> Any:
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[Any]:
        entity = self.find_by_id(entity_id)
        if not entity:
            return None
        for key, value in data.items():
            if hasattr(entity, key) and key != 'id':
                setattr(entity, key, value)
        db.session.commit()
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.find_by_id(entity_id)
        if not entity:
            return False
        db.session.delete(entity)
        db.session.commit()
        return True
