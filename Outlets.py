# --------------------------------
# OutletsSource Class
# --------------------------------
import json
import logging
from pydantic import BaseModel, Field

__name__ = "Data Source Model"
logger = logging.getLogger(__name__)


class Attributes(BaseModel):
    name: str
    url: str


class OutletsSource(BaseModel):
    attributes: Attributes

    def to_json(self) -> str:
        return json.dumps(self.dict())


class OutletsHandler(BaseModel):
    news_outlets: list[OutletsSource] = []

    def add(self, outlet: OutletsSource):
        self.news_outlets.append(outlet.attributes)

    def remove_outlet(self, key: str):
        self.news_outlets.pop(key, None)

    def get_outlet_url(self, key: str):
        return self.news_outlets.get(key)

    def get_all_outlets(self):
        return self.news_outlets

    def to_json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, json_str: str) -> "OutletsHandler":
        data = json.loads(json_str)
        return cls(**data)
