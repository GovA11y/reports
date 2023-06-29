# orgs.py
# Relative Path: insight/api/models/orgs.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ...core import Base
from .targets import Domain


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = {'schema': 'orgs'}

    id = Column(Integer, primary_key=True, index=True)  # Use sequence in PostgreSQL, like: id = Column(Integer, Sequence('fed_agencies_id_seq'), primary_key=True,)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When added
    updated_at = Column(DateTime(timezone=True), server_default=func.now())  # When row updated
    name = Column(String, unique=True)  # Entity name
    # type = Column(String, ForeignKey('refs.org_types.name'))  # What type of org is this? From refs.org_types
    acronym = Column(String)  # Entity acronym
    active = Column(Boolean, default=False)  # Is this entity active?

    # Relationships
    domains = relationship('Domain', back_populates='org')