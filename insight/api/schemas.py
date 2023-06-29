from typing import List, Optional
from pydantic import BaseModel


class Domain(BaseModel):
    id: int
    domain: str
    url_count: Optional[int]

    class Config:
        orm_mode = True
