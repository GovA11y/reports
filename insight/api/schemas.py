from pydantic import BaseModel
from typing import List

class Url(BaseModel):
    url: str
    is_objective: bool

class Domain(BaseModel):
    id: int
    domain: str
    urls: List[Url] = []

    class Config:
        orm_mode = True