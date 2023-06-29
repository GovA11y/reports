# queries.py
# Relative Path: insight/api/schemas/queries.py
from pydantic import BaseModel
from typing import Optional
from .axe import ScanData, Rule, Test


class Issue(BaseModel):
    scan_data: ScanData
    rule: Rule
    test: Test

    class Config:
        orm_mode = True


# Domain URL Count
class Domain(BaseModel):
    domain_id: int
    domain: str
    url_count: Optional[int]

    class Config:
        orm_mode = True