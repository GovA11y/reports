from typing import List, Optional
from pydantic import BaseModel


class Domain(BaseModel):
    domain_id: int
    domain: str
    url_count: Optional[int]

    class Config:
        orm_mode = True


# HTTP Error Handling Class
class HTTPError(BaseModel):
    detail: str
