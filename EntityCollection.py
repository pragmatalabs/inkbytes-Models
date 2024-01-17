import json
import logging
import sys

from typing import List, Dict
from pydantic import BaseModel, Field
sys.path.append("../")
from Models.Entities import Entity

__name__ = "Entity Collections Class"

logger = logging.getLogger(__name__)


class EntityCollection(BaseModel):
    """
    Author: Julian Delarosa (juliandelarosa@icloud.com)
    Date: 2023-07-14
    Version: 1.0
    Description:
        A class used to represent a collection of Entity objects. It extends the List class from the typing module.

    System: URIHarvest v1.0
    Language: Python 3.10
    License: GNU General Public License (GPL)

    Notes:
        - This class provides methods for adding an entity to the collection, getting entities by type,
        converting the collection to a list, removing duplicate entities, and converting the collection to a JSON string.

    Attributes
    ----------
    entities : List[Entity]
        a list of Entity objects
    """

    entities: List[Entity] = Field(default_factory=list)

    def add_entity(self, entity: Entity) -> None:
        """
        Adds an entity to the collection if it's not already in the collection.

        Parameters:
            entity (Entity): The entity to add.

        Returns:
            None
        """
        if entity not in self.entities:
            self.entities.append(entity)

    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """
        Returns a list of entities that match the given type.

        Parameters:
            entity_type (str): The type of entities to retrieve.

        Returns:
            List[Entity]: List of entities with the specified type.
        """
        return [entity for entity in self.entities if entity.type == entity_type]

    def to_list(self) -> List[Entity]:
        """
        Returns a list representation of the collection.

        Returns:
            List[Entity]: A list of entities.
        """
        return self.entities

    def remove_duplicates(self) -> None:
        """
        Removes duplicate entities from the collection.

        Returns:
            None
        """
        seen = set()
        unique_entities = []
        for entity in self.entities:
            entity_tuple = tuple(
                (k, v if not isinstance(v, dict) else tuple(v.items()))
                for k, v in entity.to_dict().items()
            )
            if entity_tuple not in seen:
                seen.add(entity_tuple)
                unique_entities.append(entity)
        self.entities = unique_entities

    def __iter__(self):
        return iter(self.entities)

    def __len__(self):
        return len(self.entities)

    @classmethod
    def from_list(cls, entities_data: List[Dict]) -> "EntityCollection":
        """
        Creates an EntityCollection from a list of dictionaries.

        Parameters:
            entities_data (List[Dict]): List of dictionaries representing entities.

        Returns:
            EntityCollection: An instance of the EntityCollection.
        """
        entity_collection = cls(entities=[])
        for entity_data in entities_data:
            entity = Entity(**entity_data)
            entity_collection.add_entity(entity)
        return entity_collection

    def to_json(self) -> str:
        """
        Returns a JSON string representation of the collection.

        Returns:
            str: JSON string representation of the collection.
        """
        return json.dumps(self.entities, indent=4, cls=EntityEncoder)

    def to_string(self) -> str:
        """
        Returns a string representation of the collection.

        Returns:
            str: String representation of the collection.
        """
        return "\n".join(str(entity) for entity in self.entities)

    @classmethod
    def from_json(cls, json_data: str) -> "EntityCollection":
        """
        Creates an EntityCollection from a JSON string.

        Parameters:
            json_data (str): JSON string representation of the collection.

        Returns:
            EntityCollection: An instance of the EntityCollection.
        """
        entities_data = json.loads(json_data)
        return cls.from_list(entities_data)

    class Config:
        arbitrary_types_allowed = True
        from_attributes: True


class EntityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return obj.to_dict()
        return super().default(obj)
