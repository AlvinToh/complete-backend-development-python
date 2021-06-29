from typing import List
from pydantic import BaseModel


class Author(BaseModel):
    name: str
    book: List[str]