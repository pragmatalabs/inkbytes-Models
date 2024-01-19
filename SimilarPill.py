from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class SimilarPill(BaseModel):
    id: Optional[str] = None
    uid: Optional[str] = None
    title: Optional[str] = None
    text: Optional[str] = None
    summary: Optional[str] = None
    related: Optional[list] = None
    similars: Optional[list] = None

    def to_dict(self):
        article_dict = self.__dict__.copy()
        return article_dict
