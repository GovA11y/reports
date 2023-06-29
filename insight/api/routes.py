from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
import io
import csv
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from ..core.database import SessionLocal, engine, Base
from ..api import models, schemas

# Create API router
router = APIRouter()

# Get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get Number of URLs for domain & sub-domains
@router.get('/count/{domain}')
def read_domain(domain: str, db: Session = Depends(get_db), output: str = 'json'):
    pattern = '%' + domain + '%'
    query_results = db.query(models.Domain.id,
                             models.Domain.domain,
                             func.count(models.Url.url)).join(
                             models.Url).filter(
                             models.Domain.domain.ilike(pattern)).group_by(
                             models.Domain.id,
                             models.Domain.domain).order_by(
                             func.count(models.Url.url).desc()).all()

    if not query_results:
        raise HTTPException(status_code=404, detail="Domain not found")

    domains = [schemas.Domain(id=domain_id,
                              domain=domain,
                              url_count=url_count)
               for domain_id, domain, url_count in query_results]

    if output == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "domain", "url_count"])
        for domain in domains:
            writer.writerow([domain.id, domain.domain, domain.url_count])
        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    else:
        return domains
