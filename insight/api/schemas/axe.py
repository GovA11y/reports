# axe.py
# Relative Path: insight/api/schemas/axe.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ScanData(BaseModel):
    id: int
    engine_name: Optional[str] = Field(None, max_length=20)
    engine_version: Optional[str] = Field(None, max_length=10)
    orientation_angle: Optional[str] = Field(None, max_length=5)
    orientation_type: Optional[str] = Field(None, max_length=25)
    user_agent: Optional[str] = Field(None, max_length=250)
    window_height: Optional[int]
    window_width: Optional[int]
    reporter: Optional[str] = Field(None, max_length=50)
    runner_name: Optional[str] = Field(None, max_length=50)
    scanned_at: Optional[datetime]
    url: Optional[str]


class Rule(BaseModel):
    id: int
    rule_type: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=250)
    help: Optional[str] = Field(None, max_length=250)
    help_url: Optional[str] = Field(None, max_length=250)
    axe_id: Optional[str] = Field(None, max_length=35)
    impact: Optional[str] = Field(None, max_length=25)
    tags: Optional[str]
    nodes: Optional[str]
    created_at: datetime


class Test(BaseModel):
    id: int
    rule_type: str
    target: str
    axe_id: str
    created_at: datetime
    active: bool
    impact: Optional[str]
    tested_at: Optional[datetime]
    html: Optional[str]
    failure_summary: Optional[str]