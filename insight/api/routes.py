from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.params import Query, Path
from pydantic import BaseModel
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
@router.get('/count/{domain}',
            summary="Number of tracked URLs by domain",
            response_model=List[schemas.Domain],
            response_description="A list of domains with their count",
            tags=["Metrics"])
def read_domain(domain: str = Path(..., description="The domain name to get the URL count"),
                db: Session = Depends(get_db),
                output: str = Query(default="json", description="The output format; can be either json or csv")):
    """
    Retrieve the number of URLs for a specific domain and its subdomains.


    **If you enter _va.gov_, test.va.gov, va.gov, and all other va.gov subdomains are counted.**
    The domain name should be provided in the path. The output format is json by default,
    but can be changed to csv.

    - **domain**: The domain name to get the URL count.
    - **db**: An instance of the database session.
    - **output**: The output format; can be either json ('json') or csv ('csv'). Default is 'json'.
    """
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

    domains = [schemas.Domain(domain_id=domain_id,
                              domain=domain,
                              url_count=url_count)
               for domain_id, domain, url_count in query_results]

    if output == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["domain_id", "domain", "url_count"])
        for domain in domains:
            writer.writerow([domain.domain_id, domain.domain, domain.url_count])
        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    else:
        return domains