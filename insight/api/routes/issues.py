# issues.py
# Relative Path: insight/api/routes/issues.py
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional
import pandas as pd
from fastapi.responses import JSONResponse
from ...core import SessionLocal, engine, Base
from .. import models, schemas
# from .webhook import rules_dict


# Create API router
router = APIRouter()


# Get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)}")


@router.get("/tests")
async def read_issues(
    output: str,
    domain: str,
    limit: Optional[int] = None,
    rule_type: Optional[str] = None,
    section508: Optional[bool] = None,
    super_waggy: Optional[bool] = None,
    db: Session = Depends(get_db),
    tags=["Issues"],
    summary="Axe Issues per Filters"
):

    sql = text(f"""
    SELECT
        t.domain_id,
        d.domain,
        t.id AS url_id,
        t.url,
        s.id AS scan_id,
        r.id AS rule_id,
        test.id AS "test_id",
        test.tested_at,
        test.rule_type,
        test.axe_id,
        test.impact,
        test.target,
       test.html,
       test.failure_summary,
       test.section508,
       test.super_waggy
    FROM targets.urls t
    INNER JOIN targets.domains d ON t.domain_id = d.id AND d.domain = :domain
    LEFT JOIN (
        SELECT url_id,
        MAX(created_at) AS max_created_at
        FROM axe.scan_data
        GROUP BY url_id
    ) latest_scan ON t.id = latest_scan.url_id
    LEFT JOIN axe.scan_data s
      ON t.id = s.url_id AND s.created_at = latest_scan.max_created_at
    INNER JOIN axe.rules r
      ON s.id = r.scan_id
    INNER JOIN axe.tests test
      ON r.id = test.rule_id
    WHERE s.id IS NOT NULL
      AND (:rule_type is NULL or test.rule_type = :rule_type)
      AND (:section508 is NULL or test.section508 = :section508)
      AND (:super_waggy is NULL or test.super_waggy = :super_waggy)
    ORDER BY test.tested_at desc
    {f'LIMIT {limit}' if limit else ''}
    """)

    result = db.execute(sql, {"domain": domain, "rule_type": rule_type, "section508": section508, "super_waggy": super_waggy}).fetchall()

    data = [
        {**{k: (custom_encoder(v) if isinstance(v, datetime) else v) for k, v in row._asdict().items()}}
        for row in result
    ]

    if output == "json":
        return JSONResponse(content=jsonable_encoder(data))
    elif output == "csv":
        df = pd.DataFrame(data)
        return Response(content=df.to_csv(index=False), media_type='text/csv')