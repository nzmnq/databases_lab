from abc import ABC
from datetime import date, datetime
from typing import List, Optional, Any, Dict
from my_project import db


def _coerce_column_value(entity: Any, key: str, value: Any) -> Any:
    if value is None or not isinstance(value, str):
        return value
    column = entity.__table__.columns.get(key)
    if column is None:
        return value
    if isinstance(column.type, db.DateTime):
        return datetime.fromisoformat(value)
    if isinstance(column.type, db.Date):
        return date.fromisoformat(value[:10])
    return value


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
            if hasattr(entity, key) and key not in ('id', 'client_id'):
                setattr(entity, key, _coerce_column_value(entity, key, value))
        db.session.commit()
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.find_by_id(entity_id)
        if not entity:
            return False
        db.session.delete(entity)
        db.session.commit()
        return True
