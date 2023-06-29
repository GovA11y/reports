from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)  # Primary domain identifier
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When domain added
    updated_at = Column(DateTime(timezone=True), server_default=func.now())  # When row updated
    domain = Column(String, unique=True, nullable=False)  # Unique domain name
    active = Column(Boolean)  # Should we analyze this domain?
    org_id = Column(Integer, ForeignKey('orgs.entities.id'))  # Corresponding Entity ID
    urls = relationship('Url', back_populates='domain')  # Relationship to urls


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)  # Use sequence in PostgreSQL, like: id = Column(Integer, Sequence('fed_agencies_id_seq'), primary_key=True,)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When added
    updated_at = Column(DateTime(timezone=True), server_default=func.now())  # When row updated
    name = Column(String, unique=True)  # Entity name
    type = Column(String, ForeignKey('refs.org_types.name'))  # What type of org is this? From refs.org_types
    acronym = Column(String)  # Entity acronym
    active = Column(Boolean, default=False)  # Is this entity active?
    domains = relationship('Domain', back_populates='org')


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)  # Add this line
    url = Column(String)
    domain_id = Column(Integer, ForeignKey('domains.id'))
    is_objective = Column(Boolean)
    domain = relationship('Domain', back_populates='urls')