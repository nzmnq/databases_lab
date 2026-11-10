from typing import Dict, Any

class IDTO:
    def put_into_dto(self) -> Dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def create_from_dto(cls, dto_dict: Dict[str, Any]):
        raise NotImplementedError
