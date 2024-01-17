import json
from typing import List, Dict, Optional
from pydantic import BaseModel

__name__ = "Entity Model Class"


class Entity(BaseModel):
    type: Optional[str]
    name: Optional[str]
    links: Optional[List[str]]

    def to_dict(self) -> Dict:
        return {
            "type": self.type or "",
            "name": self.name or "",
            "links": self.links or []
        }

    @classmethod
    def from_dict(cls, data: any):
        for entity_info in data:
            entity = Entity(**entity_info)
        return entity

    @classmethod
    def from_json(cls, json_data: str):
        data = json.loads(json_data)
        return cls.from_dict(data)

    def to_json(self) -> str:
        data = self.to_dict()
        if len(data) > 0:
            return json.dumps(data, cls=EntityEncoder)
        else:
            return "{}"

    def __hash__(self):
        return hash((self.type, self.name, tuple(self.links)))

    def __repr__(self):
        return f"Entity(type={self.type}, name={self.name}, links={self.links})"

    class Config:
        arbitrary_types_allowed = True
        orm: True


class EntityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return obj.to_dict()
        return super().default(obj)
