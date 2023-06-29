from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
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

@router.get('/{domain}', response_model=schemas.Domain)
def read_domain(domain: str, db: Session = Depends(get_db)):
    return db.query(models.Domain, func.count(models.Url.url)).join(models.Url).filter(models.Url.is_objective == True, models.Domain.domain == domain).group_by(models.Domain.id, models.Domain.domain).first()